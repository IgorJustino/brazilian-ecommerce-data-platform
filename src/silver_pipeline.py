from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_OLIST_DIR = PROJECT_ROOT / "Data Layer" / "raw" / "olist"
SILVER_DIR = PROJECT_ROOT / "Data Layer" / "silver"


def normalize_zip_prefix(series: pd.Series) -> pd.Series:
    zip_str = pd.to_numeric(series, errors="coerce").astype("Int64").astype("string")
    return zip_str.str.zfill(5)


def read_olist_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(RAW_OLIST_DIR / filename, low_memory=False)


def load_olist_datasets() -> dict[str, pd.DataFrame]:
    return {
        "customers": read_olist_csv("olist_customers_dataset.csv"),
        "orders": read_olist_csv("olist_orders_dataset.csv"),
        "order_items": read_olist_csv("olist_order_items_dataset.csv"),
        "products": read_olist_csv("olist_products_dataset.csv"),
        "translation": read_olist_csv("product_category_name_translation.csv"),
        "sellers": read_olist_csv("olist_sellers_dataset.csv"),
        "payments": read_olist_csv("olist_order_payments_dataset.csv"),
        "reviews": read_olist_csv("olist_order_reviews_dataset.csv"),
    }


def build_products_enriched(products: pd.DataFrame, translation: pd.DataFrame) -> pd.DataFrame:
    products_enriched = products.merge(
        translation,
        on="product_category_name",
        how="left",
        validate="m:1",
    )

    products_enriched["product_category_name_english"] = products_enriched[
        "product_category_name_english"
    ].fillna(products_enriched["product_category_name"])

    return products_enriched.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )


def build_payments_agg(payments: pd.DataFrame) -> pd.DataFrame:
    payment_type_totals = (
        payments.groupby(["order_id", "payment_type"], dropna=False, as_index=False)
        .agg(payment_type_value=("payment_value", "sum"))
        .sort_values(["order_id", "payment_type_value", "payment_type"], ascending=[True, False, True])
    )
    payment_type_main = (
        payment_type_totals.drop_duplicates("order_id")
        .loc[:, ["order_id", "payment_type"]]
        .rename(columns={"payment_type": "payment_type_main"})
    )

    payments_agg = (
        payments.groupby("order_id", as_index=False)
        .agg(
            payment_value_total=("payment_value", "sum"),
            payment_installments_max=("payment_installments", "max"),
            payment_methods_count=("payment_type", "nunique"),
        )
        .merge(payment_type_main, on="order_id", how="left", validate="1:1")
    )
    payments_agg["has_payment"] = True
    payments_agg["has_multiple_payment_methods"] = payments_agg["payment_methods_count"] > 1

    return payments_agg


def build_reviews_agg(reviews: pd.DataFrame) -> pd.DataFrame:
    reviews = reviews.copy()
    reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"], errors="coerce")
    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"],
        errors="coerce",
    )

    return reviews.groupby("order_id", as_index=False).agg(
        review_score=("review_score", "mean"),
        review_count=("review_id", "nunique"),
        review_creation_date=("review_creation_date", "min"),
        review_answer_timestamp=("review_answer_timestamp", "max"),
    )


def add_derived_columns(fact_sales: pd.DataFrame) -> pd.DataFrame:
    fact_sales = fact_sales.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date",
    ]
    for column in date_columns:
        fact_sales[column] = pd.to_datetime(fact_sales[column], errors="coerce")

    fact_sales["purchase_date"] = fact_sales["order_purchase_timestamp"].dt.date
    fact_sales["purchase_year"] = fact_sales["order_purchase_timestamp"].dt.year.astype("Int64")
    fact_sales["purchase_month"] = fact_sales["order_purchase_timestamp"].dt.month.astype("Int64")
    fact_sales["purchase_year_month"] = fact_sales["order_purchase_timestamp"].dt.strftime("%Y-%m")
    fact_sales["purchase_quarter"] = fact_sales["order_purchase_timestamp"].dt.quarter.astype("Int64")
    fact_sales["purchase_weekday"] = fact_sales["order_purchase_timestamp"].dt.day_name()

    fact_sales["delivery_days"] = (
        fact_sales["order_delivered_customer_date"] - fact_sales["order_purchase_timestamp"]
    ).dt.days.astype("Int64")
    fact_sales["estimated_delivery_days"] = (
        fact_sales["order_estimated_delivery_date"] - fact_sales["order_purchase_timestamp"]
    ).dt.days.astype("Int64")
    fact_sales["delivery_delay_days"] = (
        fact_sales["order_delivered_customer_date"] - fact_sales["order_estimated_delivery_date"]
    ).dt.days.astype("Int64")

    fact_sales["is_completed"] = fact_sales["order_status"].eq("delivered")
    fact_sales["is_delivered"] = fact_sales["order_delivered_customer_date"].notna()
    fact_sales["is_late"] = fact_sales["delivery_delay_days"].gt(0).fillna(False)

    fact_sales["payment_value_total"] = fact_sales["payment_value_total"].fillna(0)
    fact_sales["payment_installments_max"] = fact_sales["payment_installments_max"].fillna(0).astype("Int64")
    fact_sales["payment_methods_count"] = fact_sales["payment_methods_count"].fillna(0).astype("Int64")
    fact_sales["has_payment"] = fact_sales["has_payment"].fillna(False).astype(bool)
    fact_sales["has_multiple_payment_methods"] = (
        fact_sales["has_multiple_payment_methods"].fillna(False).astype(bool)
    )

    fact_sales["total_sale"] = fact_sales["price"]
    fact_sales["total_freight"] = fact_sales["freight_value"]
    fact_sales["total_item_value"] = fact_sales["price"] + fact_sales["freight_value"]
    fact_sales["total_order_payment"] = fact_sales["payment_value_total"]

    for zip_col in ["customer_zip_code_prefix", "seller_zip_code_prefix"]:
        fact_sales[zip_col] = normalize_zip_prefix(fact_sales[zip_col])

    return fact_sales


def build_fact_sales(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    products_enriched = build_products_enriched(datasets["products"], datasets["translation"])
    payments_agg = build_payments_agg(datasets["payments"])
    reviews_agg = build_reviews_agg(datasets["reviews"])

    fact_sales = datasets["order_items"].merge(
        datasets["orders"],
        on="order_id",
        how="inner",
        validate="m:1",
    )
    fact_sales = fact_sales.merge(
        datasets["customers"],
        on="customer_id",
        how="left",
        validate="m:1",
    )
    fact_sales = fact_sales.merge(
        products_enriched,
        on="product_id",
        how="left",
        validate="m:1",
    )
    fact_sales = fact_sales.merge(
        datasets["sellers"],
        on="seller_id",
        how="left",
        validate="m:1",
    )
    fact_sales = fact_sales.merge(
        payments_agg,
        on="order_id",
        how="left",
        validate="m:1",
    )
    fact_sales = fact_sales.merge(
        reviews_agg,
        on="order_id",
        how="left",
        validate="m:1",
    )

    fact_sales = add_derived_columns(fact_sales)

    ordered_columns = [
        "order_id",
        "order_item_id",
        "customer_id",
        "customer_unique_id",
        "product_id",
        "seller_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
        "product_category_name",
        "product_category_name_english",
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
        "price",
        "freight_value",
        "payment_value_total",
        "payment_installments_max",
        "payment_methods_count",
        "payment_type_main",
        "has_payment",
        "has_multiple_payment_methods",
        "review_score",
        "review_count",
        "review_creation_date",
        "review_answer_timestamp",
        "purchase_date",
        "purchase_year",
        "purchase_month",
        "purchase_year_month",
        "purchase_quarter",
        "purchase_weekday",
        "delivery_days",
        "estimated_delivery_days",
        "delivery_delay_days",
        "is_completed",
        "is_delivered",
        "is_late",
        "total_sale",
        "total_freight",
        "total_item_value",
        "total_order_payment",
    ]

    return fact_sales.loc[:, ordered_columns].sort_values(["order_id", "order_item_id"]).reset_index(drop=True)


def validate_fact_sales(fact_sales: pd.DataFrame, order_items: pd.DataFrame) -> None:
    expected_rows = len(order_items)
    if len(fact_sales) != expected_rows:
        raise ValueError(f"Row count mismatch: expected {expected_rows}, got {len(fact_sales)}")

    duplicated_key_count = int(fact_sales.duplicated(["order_id", "order_item_id"]).sum())
    if duplicated_key_count:
        raise ValueError(f"Duplicated logical keys found: {duplicated_key_count}")

    if fact_sales["order_id"].isna().any() or fact_sales["order_item_id"].isna().any():
        raise ValueError("Logical key contains null values")


def write_outputs(fact_sales_olist: pd.DataFrame) -> list[Path]:
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    csv_path = SILVER_DIR / "fact_sales_olist.csv"
    fact_sales_olist.to_csv(csv_path, index=False)
    outputs.append(csv_path)

    parquet_path = SILVER_DIR / "fact_sales_olist.parquet"
    try:
        fact_sales_olist.to_parquet(parquet_path, index=False)
    except ImportError:
        pass
    else:
        outputs.append(parquet_path)

    return outputs


def main() -> None:
    datasets = load_olist_datasets()
    fact_sales_olist = build_fact_sales(datasets)
    validate_fact_sales(fact_sales_olist, datasets["order_items"])
    outputs = write_outputs(fact_sales_olist)

    print(f"fact_sales_olist rows: {len(fact_sales_olist)}")
    print(f"fact_sales_olist columns: {len(fact_sales_olist.columns)}")
    print(
        "duplicated logical keys: "
        f"{int(fact_sales_olist.duplicated(['order_id', 'order_item_id']).sum())}"
    )
    print(f"memory_mb: {fact_sales_olist.memory_usage(deep=True).sum() / 1024**2:.2f}")
    for output in outputs:
        print(f"written: {output.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
