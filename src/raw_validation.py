from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "Data Layer" / "raw"
REPORT_PATH = PROJECT_ROOT / "docs" / "raw_validation_report.md"

EXPECTED_DATASETS = {
    "ecommerce_2024/Amazon Sale Report.csv",
    "ecommerce_2024/Cloud Warehouse Compersion Chart.csv",
    "ecommerce_2024/Expense IIGF.csv",
    "ecommerce_2024/International sale Report.csv",
    "ecommerce_2024/May-2022.csv",
    "ecommerce_2024/P  L March 2021.csv",
    "ecommerce_2024/Sale Report.csv",
    "olist/olist_customers_dataset.csv",
    "olist/olist_geolocation_dataset.csv",
    "olist/olist_order_items_dataset.csv",
    "olist/olist_order_payments_dataset.csv",
    "olist/olist_order_reviews_dataset.csv",
    "olist/olist_orders_dataset.csv",
    "olist/olist_products_dataset.csv",
    "olist/olist_sellers_dataset.csv",
    "olist/product_category_name_translation.csv",
}

RELATIONSHIP_CHECKS = [
    (
        "orders.customer_id -> customers.customer_id",
        "olist/olist_orders_dataset.csv",
        "customer_id",
        "olist/olist_customers_dataset.csv",
        "customer_id",
    ),
    (
        "order_items.order_id -> orders.order_id",
        "olist/olist_order_items_dataset.csv",
        "order_id",
        "olist/olist_orders_dataset.csv",
        "order_id",
    ),
    (
        "order_payments.order_id -> orders.order_id",
        "olist/olist_order_payments_dataset.csv",
        "order_id",
        "olist/olist_orders_dataset.csv",
        "order_id",
    ),
    (
        "order_reviews.order_id -> orders.order_id",
        "olist/olist_order_reviews_dataset.csv",
        "order_id",
        "olist/olist_orders_dataset.csv",
        "order_id",
    ),
    (
        "order_items.product_id -> products.product_id",
        "olist/olist_order_items_dataset.csv",
        "product_id",
        "olist/olist_products_dataset.csv",
        "product_id",
    ),
    (
        "order_items.seller_id -> sellers.seller_id",
        "olist/olist_order_items_dataset.csv",
        "seller_id",
        "olist/olist_sellers_dataset.csv",
        "seller_id",
    ),
    (
        "products.product_category_name -> translation.product_category_name",
        "olist/olist_products_dataset.csv",
        "product_category_name",
        "olist/product_category_name_translation.csv",
        "product_category_name",
    ),
]


@dataclass(frozen=True)
class DatasetProfile:
    name: str
    path: Path
    rows: int
    columns: int
    duplicate_rows: int
    memory_mb: float
    dtypes: dict[str, str]
    nulls: dict[str, int]


def read_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8", "utf-8-sig", "latin1"):
        try:
            return pd.read_csv(path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="latin1", low_memory=False)


def relative_dataset_name(path: Path) -> str:
    return path.relative_to(RAW_DIR).as_posix()


def discover_csv_files() -> list[Path]:
    return sorted(RAW_DIR.rglob("*.csv"))


def profile_dataset(name: str, path: Path, df: pd.DataFrame) -> DatasetProfile:
    return DatasetProfile(
        name=name,
        path=path,
        rows=len(df),
        columns=len(df.columns),
        duplicate_rows=int(df.duplicated().sum()),
        memory_mb=float(df.memory_usage(deep=True).sum() / 1024**2),
        dtypes={column: str(dtype) for column, dtype in df.dtypes.items()},
        nulls={column: int(value) for column, value in df.isna().sum().items()},
    )


def validate_relationships(datasets: dict[str, pd.DataFrame]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    for label, child_name, child_key, parent_name, parent_key in RELATIONSHIP_CHECKS:
        child = datasets.get(child_name)
        parent = datasets.get(parent_name)

        if child is None or parent is None:
            results.append(
                {
                    "relationship": label,
                    "status": "missing_dataset",
                    "missing_keys": None,
                    "missing_ratio": None,
                    "sample_missing_values": "n/a",
                }
            )
            continue

        child_values = child[child_key].dropna()
        parent_values = parent[parent_key].dropna()
        missing_mask = ~child_values.isin(parent_values)
        missing_count = int(missing_mask.sum())
        total = int(len(child_values))
        sample_missing_values = sorted(child_values.loc[missing_mask].astype(str).unique())[:10]

        results.append(
            {
                "relationship": label,
                "status": "ok" if missing_count == 0 else "failed",
                "missing_keys": missing_count,
                "missing_ratio": missing_count / total if total else 0,
                "sample_missing_values": ", ".join(sample_missing_values) if sample_missing_values else "",
            }
        )

    return results


def markdown_table(headers: Iterable[str], rows: Iterable[Iterable[object]]) -> str:
    header_list = list(headers)
    lines = [
        "| " + " | ".join(header_list) + " |",
        "| " + " | ".join("---" for _ in header_list) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def format_dtypes(profile: DatasetProfile) -> str:
    rows = sorted(profile.dtypes.items())
    return markdown_table(["coluna", "tipo"], rows)


def format_nulls(profile: DatasetProfile) -> str:
    rows = [
        (column, value, f"{value / profile.rows:.2%}" if profile.rows else "0.00%")
        for column, value in sorted(profile.nulls.items(), key=lambda item: item[1], reverse=True)
        if value > 0
    ]
    if not rows:
        return "Nenhum valor nulo identificado."
    return markdown_table(["coluna", "nulos", "%"], rows)


def build_report(
    profiles: list[DatasetProfile],
    missing_datasets: list[str],
    unexpected_datasets: list[str],
    relationship_results: list[dict[str, object]],
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_rows = sum(profile.rows for profile in profiles)
    total_memory = sum(profile.memory_mb for profile in profiles)

    summary_rows = [
        (
            profile.name,
            profile.rows,
            profile.columns,
            profile.duplicate_rows,
            f"{profile.memory_mb:.2f}",
        )
        for profile in profiles
    ]

    relationship_rows = [
        (
            result["relationship"],
            result["status"],
            result["missing_keys"],
            f"{result['missing_ratio']:.4%}" if result["missing_ratio"] is not None else "n/a",
            result["sample_missing_values"],
        )
        for result in relationship_results
    ]

    sections = [
        "# Relatorio de Validacao da RAW",
        "",
        f"Gerado em: `{generated_at}`",
        "",
        "## Resumo",
        "",
        f"- Datasets esperados: {len(EXPECTED_DATASETS)}",
        f"- Datasets encontrados: {len(profiles)}",
        f"- Total de registros carregados: {total_rows}",
        f"- Memoria estimada em pandas: {total_memory:.2f} MB",
        f"- Datasets ausentes: {len(missing_datasets)}",
        f"- Datasets inesperados: {len(unexpected_datasets)}",
        "",
        "## Existencia dos datasets",
        "",
        "Todos os datasets esperados foram encontrados."
        if not missing_datasets
        else markdown_table(["dataset ausente"], [(item,) for item in missing_datasets]),
        "",
        "## Datasets inesperados",
        "",
        "Nenhum dataset inesperado foi encontrado."
        if not unexpected_datasets
        else markdown_table(["dataset inesperado"], [(item,) for item in unexpected_datasets]),
        "",
        "## Quantidade de registros, colunas e duplicidades",
        "",
        markdown_table(
            ["dataset", "registros", "colunas", "linhas duplicadas", "memoria_mb"],
            summary_rows,
        ),
        "",
        "## Chaves de relacionamento",
        "",
        markdown_table(
            ["relacionamento", "status", "chaves ausentes", "% ausente", "amostra ausente"],
            relationship_rows,
        ),
    ]

    for profile in profiles:
        sections.extend(
            [
                "",
                f"## {profile.name}",
                "",
                "### Tipos das colunas",
                "",
                format_dtypes(profile),
                "",
                "### Valores nulos",
                "",
                format_nulls(profile),
            ]
        )

    return "\n".join(sections) + "\n"


def main() -> None:
    csv_files = discover_csv_files()
    found_names = {relative_dataset_name(path) for path in csv_files}
    missing_datasets = sorted(EXPECTED_DATASETS - found_names)
    unexpected_datasets = sorted(found_names - EXPECTED_DATASETS)

    datasets: dict[str, pd.DataFrame] = {}
    profiles: list[DatasetProfile] = []

    for path in csv_files:
        name = relative_dataset_name(path)
        df = read_csv(path)
        datasets[name] = df
        profiles.append(profile_dataset(name, path, df))

    relationship_results = validate_relationships(datasets)
    report = build_report(profiles, missing_datasets, unexpected_datasets, relationship_results)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    failed_relationships = [item for item in relationship_results if item["status"] != "ok"]
    print(f"Datasets carregados: {len(profiles)}")
    print(f"Datasets ausentes: {len(missing_datasets)}")
    print(f"Datasets inesperados: {len(unexpected_datasets)}")
    print(f"Relacionamentos com falha: {len(failed_relationships)}")
    print(f"Relatorio: {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
