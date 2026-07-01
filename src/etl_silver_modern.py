from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_MODERN_DIR = PROJECT_ROOT / "Data Layer" / "raw" / "ecommerce_2024"
SILVER_DIR = PROJECT_ROOT / "Data Layer" / "silver"


def read_modern_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(RAW_MODERN_DIR / filename, low_memory=False)


def normalize_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def normalize_postal_code(series: pd.Series) -> pd.Series:
    zip_num = pd.to_numeric(series, errors="coerce").astype("Int64").astype("string")
    return zip_num.str.zfill(6)


def build_sale_dimension(sale_report: pd.DataFrame) -> pd.DataFrame:
    sale = sale_report.copy()
    sale["sku_norm"] = normalize_text(sale["SKU Code"]).str.upper()
    sale["style_dim"] = normalize_text(sale["Design No."]).str.upper()
    sale["category_dim"] = normalize_text(sale["Category"])
    sale["size_dim"] = normalize_text(sale["Size"])
    sale["color_dim"] = normalize_text(sale["Color"])
    sale["stock_available"] = pd.to_numeric(sale["Stock"], errors="coerce")

    sale = sale.loc[
        :,
        [
            "sku_norm",
            "style_dim",
            "category_dim",
            "size_dim",
            "color_dim",
            "stock_available",
        ],
    ]

    # Normaliza duplicidades de SKU mantendo informacoes mais completas.
    return (
        sale.sort_values(["sku_norm", "stock_available"], ascending=[True, False])
        .drop_duplicates(subset=["sku_norm"], keep="first")
        .reset_index(drop=True)
    )


def build_fact_sales_modern(amazon_sale_report: pd.DataFrame, sale_dim: pd.DataFrame) -> pd.DataFrame:
    amz = amazon_sale_report.copy()

    rename_map = {
        "Order ID": "order_id",
        "Date": "order_date",
        "Status": "order_status",
        "Fulfilment": "fulfillment",
        "Sales Channel ": "sales_channel",
        "ship-service-level": "ship_service_level",
        "Style": "style",
        "SKU": "sku",
        "Category": "category",
        "Size": "size",
        "ASIN": "asin",
        "Courier Status": "courier_status",
        "Qty": "quantity",
        "currency": "currency",
        "Amount": "amount",
        "ship-city": "ship_city",
        "ship-state": "ship_state",
        "ship-postal-code": "ship_postal_code",
        "ship-country": "ship_country",
        "promotion-ids": "promotion_ids",
        "B2B": "is_b2b",
        "fulfilled-by": "fulfilled_by",
    }

    amz = amz.rename(columns=rename_map)

    amz["order_id"] = normalize_text(amz["order_id"])
    amz["order_date"] = pd.to_datetime(amz["order_date"], format="%m-%d-%y", errors="coerce")
    amz["order_status"] = normalize_text(amz["order_status"])
    amz["courier_status"] = normalize_text(amz["courier_status"])
    amz["fulfillment"] = normalize_text(amz["fulfillment"])
    amz["sales_channel"] = normalize_text(amz["sales_channel"])
    amz["ship_service_level"] = normalize_text(amz["ship_service_level"])
    amz["style"] = normalize_text(amz["style"]).str.upper()
    amz["sku"] = normalize_text(amz["sku"]).str.upper()
    amz["category"] = normalize_text(amz["category"])
    amz["size"] = normalize_text(amz["size"])
    amz["asin"] = normalize_text(amz["asin"])
    amz["currency"] = normalize_text(amz["currency"]).fillna("INR")
    amz["ship_city"] = normalize_text(amz["ship_city"])
    amz["ship_state"] = normalize_text(amz["ship_state"])
    amz["ship_country"] = normalize_text(amz["ship_country"])
    amz["promotion_ids"] = normalize_text(amz["promotion_ids"])
    amz["fulfilled_by"] = normalize_text(amz["fulfilled_by"])

    amz["quantity"] = pd.to_numeric(amz["quantity"], errors="coerce").fillna(0).astype("Int64")
    amz["amount"] = pd.to_numeric(amz["amount"], errors="coerce").fillna(0)
    amz["ship_postal_code"] = normalize_postal_code(amz["ship_postal_code"])
    amz["is_b2b"] = amz["is_b2b"].fillna(False).astype(bool)

    amz["sku_norm"] = amz["sku"]
    amz = amz.merge(sale_dim, on="sku_norm", how="left", validate="m:1")

    amz["style"] = amz["style"].fillna(amz["style_dim"])
    amz["category"] = amz["category"].fillna(amz["category_dim"])
    amz["size"] = amz["size"].fillna(amz["size_dim"])

    amz["order_year"] = amz["order_date"].dt.year.astype("Int64")
    amz["order_month"] = amz["order_date"].dt.month.astype("Int64")
    amz["order_year_month"] = amz["order_date"].dt.strftime("%Y-%m")

    amz["unit_price"] = amz["amount"].where(amz["quantity"] <= 0, amz["amount"] / amz["quantity"])
    amz["gross_revenue"] = amz["amount"]
    amz["is_cancelled"] = amz["order_status"].str.contains("cancel", case=False, na=False)
    amz["is_returned"] = amz["order_status"].str.contains("return", case=False, na=False)
    amz["is_delivered"] = amz["order_status"].str.contains("delivered", case=False, na=False)

    amz = amz.sort_values(["order_id", "order_date", "sku", "index"]).reset_index(drop=True)
    amz["order_item_id"] = amz.groupby("order_id").cumcount() + 1

    columns = [
        "order_id",
        "order_item_id",
        "order_date",
        "order_year",
        "order_month",
        "order_year_month",
        "order_status",
        "courier_status",
        "fulfillment",
        "sales_channel",
        "ship_service_level",
        "sku",
        "style",
        "asin",
        "category",
        "size",
        "color_dim",
        "quantity",
        "unit_price",
        "gross_revenue",
        "currency",
        "ship_city",
        "ship_state",
        "ship_postal_code",
        "ship_country",
        "promotion_ids",
        "is_b2b",
        "fulfilled_by",
        "stock_available",
        "is_cancelled",
        "is_returned",
        "is_delivered",
    ]

    fact_sales_modern = amz.loc[:, columns].rename(columns={"color_dim": "color"})
    return fact_sales_modern


def validate_fact_sales_modern(fact_sales_modern: pd.DataFrame) -> None:
    if fact_sales_modern["order_id"].isna().any():
        raise ValueError("order_id contem valores nulos")

    duplicated_key_count = int(fact_sales_modern.duplicated(["order_id", "order_item_id"]).sum())
    if duplicated_key_count:
        raise ValueError(f"Duplicidade de chave logica encontrada: {duplicated_key_count}")


def write_outputs(fact_sales_modern: pd.DataFrame) -> list[Path]:
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    csv_path = SILVER_DIR / "fact_sales_modern.csv"
    fact_sales_modern.to_csv(csv_path, index=False)
    outputs.append(csv_path)

    parquet_path = SILVER_DIR / "fact_sales_modern.parquet"
    try:
        fact_sales_modern.to_parquet(parquet_path, index=False)
    except ImportError:
        pass
    else:
        outputs.append(parquet_path)

    return outputs


def main() -> None:
    amazon_sale_report = read_modern_csv("Amazon Sale Report.csv")
    sale_report = read_modern_csv("Sale Report.csv")

    sale_dim = build_sale_dimension(sale_report)
    fact_sales_modern = build_fact_sales_modern(amazon_sale_report, sale_dim)

    validate_fact_sales_modern(fact_sales_modern)
    outputs = write_outputs(fact_sales_modern)

    print(f"fact_sales_modern rows: {len(fact_sales_modern)}")
    print(f"fact_sales_modern columns: {len(fact_sales_modern.columns)}")
    print(
        "duplicated logical keys: "
        f"{int(fact_sales_modern.duplicated(['order_id', 'order_item_id']).sum())}"
    )
    print(f"null order_date: {int(fact_sales_modern['order_date'].isna().sum())}")
    print(f"total gross_revenue: {fact_sales_modern['gross_revenue'].sum():.2f}")
    for output in outputs:
        print(f"written: {output.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()