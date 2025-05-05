"""
LLM interaction subpackage for Salesforce permission evaluation and classification.

This module provides unified imports for chat session management, category and risk evaluation,
and classification utilities used throughout the project.
"""

from .chat_session import create_chat_session

from .description_evaluator import (
    description_eval_summary,
    QualityRating
)

from .description_classifier import classify_description

from .risk_evaluator import (
    risk_eval_summary,
    RiskRating
)

from .risk_classifier import classify_risk_rating

from .category_evaluator import (
    category_eval_summary,
    CategoryRating,
    CategoryLabel,
)

from .category_classifier import classify_category

from .cloud_evaluator import (
    cloud_eval_summary,
    CloudRating
)

from .cloud_classifier import classify_cloud


__all__ = [
    'create_chat_session',

    'description_eval_summary',
    'QualityRating',
    'classify_description',

    'category_eval_summary',
    'CategoryRating',
    'CategoryLabel',
    'classify_category',

    'risk_eval_summary',
    'RiskRating',
    'classify_risk_rating',

    'cloud_eval_summary',
    'CloudRating',
    'classify_cloud'
] 