# your_package/cli.py

import typer
from niwa_api.tideclient import TideAPIClient
import os
from typing import Optional

app = typer.Typer(help="Command-line utility for the NIWA Tide API.")

@app.command()
def get_tide_data(
    lat: float = typer.Option(..., help="Latitude of the location."),
    long: float = typer.Option(..., help="Longitude of the location."),
    api_key: str = typer.Option(
        None,
        help="API key for the NIWA Tide API.",
        envvar="NIWA_API_KEY",
        prompt=True,
        hide_input=True,
    ),
    number_of_days: int = typer.Option(
        2, min=1, max=31, help="Number of days to retrieve data for (1-31)."
    ),
    start_date: Optional[str] = typer.Option(
        None, help="Start date in YYYY-MM-DD format."
    ),
    datum: str = typer.Option(
        "MSL", help="Datum to use (LAT or MSL).", case_sensitive=False
    ),
    interval: Optional[int] = typer.Option(
        None, help="Output time interval in minutes (10 to 1440)."
    ),
    format: str = typer.Option(
        "json",
        help="Output format.",
        case_sensitive=False,
        show_choices=True,
        metavar="FORMAT",
        rich_help_panel="Output Options",
    ),
    output: Optional[str] = typer.Option(
        None,
        help="Output file path. If not specified, output will be printed to stdout.",
        rich_help_panel="Output Options",
    ),
):
    """
    Fetch tide data or charts from the NIWA Tide API.
    """
    client = TideAPIClient(api_key=api_key)

    format_lower = format.lower()

    try:
        if format_lower == "json":
            data = client.get_data(
                lat=lat,
                long=long,
                number_of_days=number_of_days,
                start_date=start_date,
                datum=datum,
                interval=interval,
            )
            output_str = typer.style(str(data), fg=typer.colors.GREEN)
        elif format_lower == "csv":
            output_str = client.get_data_csv(
                lat=lat,
                long=long,
                number_of_days=number_of_days,
                start_date=start_date,
                datum=datum,
                interval=interval,
            )
        elif format_lower == "png":
            output_data = client.get_chart_png(
                lat=lat,
                long=long,
                number_of_days=number_of_days,
                start_date=start_date,
                datum=datum,
            )
        elif format_lower == "svg":
            output_str = client.get_chart_svg(
                lat=lat,
                long=long,
                number_of_days=number_of_days,
                start_date=start_date,
                datum=datum,
            )
        else:
            typer.echo(f"Error: Unsupported format '{format}'", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An error occurred: {e}", err=True)
        raise typer.Exit(code=1)

    # Output the data
    if output:
        # Write to a file
        if format_lower in ["png"]:
            with open(output, "wb") as f:
                f.write(output_data)
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_str)
        typer.echo(f"Output written to {output}")
    else:
        # Print to stdout
        if format_lower in ["png"]:
            typer.echo(
                "Binary data cannot be printed to stdout. Please specify an output file using --output.",
                err=True,
            )
            raise typer.Exit(code=1)
        else:
            typer.echo(output_str)

if __name__ == "__main__":
    app()