import argparse
import datetime
from homeharvest import scrape_property


def main():
    parser = argparse.ArgumentParser(description="Home Harvest Property Scraper")
    parser.add_argument(
        "location", type=str, help="Location to scrape (e.g., San Francisco, CA)"
    )
    parser.add_argument(
        "--site_name",
        type=str,
        nargs="*",
        default=None,
        help="Site name(s) to scrape from (e.g., realtor.com zillow)",
    )
    parser.add_argument(
        "--listing_type",
        type=str,
        default="for_sale",
        choices=["for_sale", "for_rent", "sold"],
        help="Listing type to scrape",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="excel",
        choices=["excel", "csv"],
        help="Output format",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Name of the output file (without extension)",
    )

    args = parser.parse_args()
    result = scrape_property(args.location, args.site_name, args.listing_type)

    if not args.filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        args.filename = f"HomeHarvest_{timestamp}"

    if args.output == "excel":
        output_filename = f"{args.filename}.xlsx"
        result.to_excel(output_filename, index=False)
        print(f"Excel file saved as {output_filename}")
    elif args.output == "csv":
        output_filename = f"{args.filename}.csv"
        result.to_csv(output_filename, index=False)
        print(f"CSV file saved as {output_filename}")


if __name__ == "__main__":
    main()