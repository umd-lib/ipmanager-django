import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


# converting the rails time format to the Django format using datetime
def parse_time(value):
    if not value:
        return None
    date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
    return date.isoformat() + 'Z'


# converting the rails boolean format to the Django format
def parse_bool(value):
    return str(value) == 't'


# formatting the rails JSON into the Django fixture JSON for specifically the groups.csv file
def groups_converting(row):
    return {
        'model': 'api.group',
        'pk': int(row['id']),
        'fields': {
            'created': parse_time(row['created_at']),
            'modified': parse_time(row['updated_at']),
            'key': row['key'],
            'name': row['name'],
            'description': row['description'],
            'notes': row['notes'],
            'export': parse_bool(row['export']),
        },
    }


# formatting the rails JSON into the Django fixture JSON for specifically the ip_ranges.csv file
def ip_ranges_converting(row):
    return {
        'model': 'api.iprange',
        'pk': int(row['id']),
        'fields': {
            'created': parse_time(row['created_at']),
            'modified': parse_time(row['updated_at']),
            'group': int(row['group_id']) if 'group_id' in row else None,
            'value': row['value'],
        },
    }


# formatting the rails JSON into the Django fixture JSON for specifically the relations.csv file
def relations_converting(row):
    return {
        'model': 'api.relation',
        'pk': int(row['id']),
        'fields': {
            'created': parse_time(row['created_at']),
            'modified': parse_time(row['updated_at']),
            'subject': int(row['subject_id']) if 'subject_id' in row else None,
            'object': int(row['object_id']) if 'object_id' in row else None,
            'relation': int(row['relation_type']) if 'relation_type' in row else None,
        },
    }


class Command(BaseCommand):
    help = 'Read the CSV file and create fixture data.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=Path, help='src/ipmanager/groups.csv')

        parser.add_argument(
            '--kind',
            choices=['group', 'iprange', 'relation'],
            help='Type of CSV: group, iprange, or relation.',
        )

        parser.add_argument('--output', '-o', type=Path, required=True)

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])
        kind = options['kind']

        self.stdout.write(f'File path is: {file_path}')

        if not file_path.exists():
            raise CommandError(f'File not found: {file_path}')

        if kind == 'group':
            converter = groups_converting
        elif kind == 'iprange':
            converter = ip_ranges_converting
        else:
            converter = relations_converting

        fixture_objects = self.convert_csv(file_path, converter)
        for obj in fixture_objects:
            self.stdout.write(str(obj))
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed row with {converter.__name__}'
                )
            )

        output_file = options['output']
        with output_file.open('w', encoding='utf-8') as out_file:
            import json

            json.dump(fixture_objects, out_file, indent=4)
        self.stdout.write(self.style.SUCCESS(f'Fixture data written to {output_file}'))

    def convert_csv(self, file_path, converter):
        """Read CSV files and convert using the given converter"""

        objects = []
        with file_path.open(newline='', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                self.stdout.write(str(row))
                fixture_obj = converter(row)
                objects.append(fixture_obj)
            return objects
