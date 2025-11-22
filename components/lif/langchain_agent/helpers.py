"""
Module for saving interactions summary data about a person to a GraphQL endpoint.

This module provides a function to save interaction summary data about a person,
including the conversation summary and other metadata
to a specified GraphQL server.
"""

from string import Template

import requests

from lif.logging import get_logger

logger = get_logger(__name__)


def _build_mutation_query(identifier: str, identifier_type: str, data: dict) -> str:
    """
    Builds the GraphQL query string for updating data with a specific identifier and type.
    """
    query = Template(
        """
      mutation MyMutation {
      updatePerson(
        filter: {identifier: {identifier: "$identifier", identifierType: $identifier_type}}
        input: {
          interactions: {
            channel: $channel, 
            channelIdentifier: "$channel_identifier", 
            channelIdentifierType: $channel_identifier_type, 
            followupRequired: $followup_required, 
            interactionEnd: "$interaction_end_date", 
            interactionId: "$interaction_id", 
            interactionStart: "$interaction_start_date", 
            interactionType: $interaction_type, 
            sentiment: $sentiment, 
            severity: $severity, 
            summary: "$summary"
          }
        }
      ) {
        interactions {
          channel
          channelIdentifier
          channelIdentifierType
          followupRequired
          interactionEnd
          interactionId
          interactionStart
          sentiment
          interactionType
          severity
          summary
        }
      }
    }
    """
    )

    return query.substitute(
        identifier=identifier,
        identifier_type=identifier_type,
        channel=data["channel"],
        channel_identifier=data["channel_identifier"],
        channel_identifier_type=data["channel_identifier_type"],
        followup_required=str(data["followup_required"]).lower(),
        interaction_end_date=data["interaction_end_date"],
        interaction_id=data["interaction_id"],
        interaction_start_date=data["interaction_start_date"],
        interaction_type=data["interaction_type"],
        sentiment=data["sentiment"],
        severity=data["severity"],
        summary=data["summary"].replace('"', '\\"'),
    )


def update_person_interactions(identifier: str, identifier_type: str, data: dict, graphql_url: str) -> dict | None:
    """
    Posts to a GraphQL endpoint to update interaction summary data for a person.

    Args:
        identifier (str): The identifier of the person to query.
        identifier_type (str): The type of identifier (e.g., 'SCHOOL_ASSIGNED_NUMBER').
        data (dict): The interaction summary dict
        graphql_url (str): The URL of the GraphQL endpoint.

    Returns:
        dict | None: The data returned by the GraphQL endpoint, or None if the request fails.

    Raises:
        requests.RequestException: If an error occurs during the HTTP request.
    """
    query = _build_mutation_query(identifier, identifier_type, data)
    logger.debug(query)
    try:
        response = requests.post(url=graphql_url, json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error saving data to GraphQL endpoint: {e}")
        return None
