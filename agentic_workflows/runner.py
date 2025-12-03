import click
from .core.orchestrator import Orchestrator

@click.group()
def cli():
    pass

@cli.command("run")
@click.option("--spec", "-s", required=True, help="Path to workflow spec YAML")
@click.option("--dry-run/--no-dry-run", default=True, help="Show plan only")
@click.option("--audit", default="audit.log", help="Audit log path")
def run(spec, dry_run, audit):
    orch = Orchestrator(audit_path=audit)
    out = orch.run_spec(spec, dry_run=dry_run)
    click.echo("Run complete. Summary:")
    click.echo(out)

if __name__ == "__main__":
    cli()
