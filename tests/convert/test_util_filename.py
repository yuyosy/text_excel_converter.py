
import pytest

from app.convert.util_filename import replace_datetime_to_placeholder


@pytest.mark.parametrize(('stings', 'format', 'placeholder', 'matched'), [
    ('20220101-12h34m45s', '%Y%m%d-%Hh%Mm%Ss', '${generate_datetime}', '20220101-12h34m45s'),
    ('2022', '%Y', '${generate_datetime}', '2022'),
    ('Filename_20220101-12h34m45s.txt', '%Y%m%d-%Hh%Mm%Ss', 'Filename_${generate_datetime}.txt', '20220101-12h34m45s'),
])
def test_replace_datetime_to_placeholder(stings, format, placeholder, matched):
    assert replace_datetime_to_placeholder(stings, format=format) == (placeholder, matched)
