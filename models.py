from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex
# Imports go here.


class U15EmailKeys(Model):
    """Defines the e-mail keys for U15."""
    class Meta:
        table_name = "u15_email_keys"
        region = "eu-west-2"

    key = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()


class U15HitCounter(Model):
    """Defines the hit counters for U15."""
    class Meta:
        table_name = "u15_hit_counters"
        region = "eu-west-2"

    counter_id = UnicodeAttribute(hash_key=True)
    count = NumberAttribute()


class ScoreIndex(GlobalSecondaryIndex):
    """This defines the index for the score."""
    class Meta:
        index_name = "score-index"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    score = NumberAttribute(hash_key=True)


class GlobalScoreboard(Model):
    """Defines the global scoreboard for the guessing game."""
    class Meta:
        table_name = "global_scoreboard_guessing_game"
        region = "eu-west-2"

    score = NumberAttribute()
    score_index = ScoreIndex()
    seconds = NumberAttribute()
