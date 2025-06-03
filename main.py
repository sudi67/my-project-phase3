import sys

if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
    
    sys.argv.pop(1)
    from health_tracker.cli_interactive import interactive

    if __name__ == '__main__':
        interactive()
else:
    from health_tracker.cli_simple import cli

    if __name__ == '__main__':
        cli()
