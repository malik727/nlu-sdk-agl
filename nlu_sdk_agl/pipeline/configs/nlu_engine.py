from __future__ import unicode_literals

from nlu_sdk_agl.common.from_dict import FromDict
from nlu_sdk_agl.constants import CUSTOM_ENTITY_PARSER_USAGE
from nlu_sdk_agl.entity_parser import CustomEntityParserUsage
from nlu_sdk_agl.pipeline.configs import ProcessingUnitConfig
from nlu_sdk_agl.resources import merge_required_resources


class NLUEngineConfig(FromDict, ProcessingUnitConfig):
    """Configuration of a :class:`.SnipsNLUEngine` object

    Args:
        intent_parsers_configs (list): List of intent parser configs
            (:class:`.ProcessingUnitConfig`). The order in the list determines
            the order in which each parser will be called by the nlu engine.
    """

    def __init__(self, intent_parsers_configs=None, random_seed=None):
        from nlu_sdk_agl.intent_parser import IntentParser

        if intent_parsers_configs is None:
            from nlu_sdk_agl.pipeline.configs import (
                ProbabilisticIntentParserConfig,
                DeterministicIntentParserConfig)
            intent_parsers_configs = [
                DeterministicIntentParserConfig(),
                ProbabilisticIntentParserConfig()
            ]
        self.intent_parsers_configs = [
            IntentParser.get_config(conf) for conf in intent_parsers_configs]
        self.random_seed = random_seed

    @property
    def unit_name(self):
        from nlu_sdk_agl.nlu_engine.nlu_engine import SnipsNLUEngine
        return SnipsNLUEngine.unit_name

    def get_required_resources(self):
        # Resolving custom slot values must be done without stemming
        resources = {
            CUSTOM_ENTITY_PARSER_USAGE: CustomEntityParserUsage.WITHOUT_STEMS
        }
        for config in self.intent_parsers_configs:
            resources = merge_required_resources(
                resources, config.get_required_resources())
        return resources

    def to_dict(self):
        return {
            "unit_name": self.unit_name,
            "intent_parsers_configs": [
                config.to_dict() for config in self.intent_parsers_configs
            ]
        }
