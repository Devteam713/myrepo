"""
Alethia Lifecycle Manager

Coordinates the full lifecycle of data objects within the Alethia Protocol.

Responsibilities:
- Data ingestion and registration
- Context and trust evaluation
- Entropy application and semantic transformation
- Monitoring semantic state changes over time
- Post-exfiltration survivability tracking
- Batch and streaming data support

Author: Sentenial-X Alethia Core Team
"""

from typing import List, Dict, Any
from core.orchestration.alethia_runtime import AlethiaRuntime


class LifecycleManager:
    """
    High-level lifecycle manager for Alethia-protected data.
    """

    def __init__(self, entropy_profile: Dict[str, float] = None):
        """
        Args:
            entropy_profile: Optional entropy profile to pass to the runtime.
        """
        self.runtime = AlethiaRuntime(entropy_profile=entropy_profile)
        self.data_registry: Dict[str, Dict[str, Any]] = {}

    def register_data(self, data_object: Dict[str, Any]) -> str:
        """
        Register a new data object in the lifecycle manager.

        Args:
            data_object: Dict with keys 'data_id', 'semantic_payload', and 'context_vector'

        Returns:
            data_id of the registered object
        """
        data_id = data_object.get("data_id")
        if not data_id:
            raise ValueError("Data object must have a 'data_id' field.")

        self.data_registry[data_id] = data_object
        return data_id

    def ingest(self, data_object: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest and process a data object through the full Alethia runtime pipeline.

        Args:
            data_object: Data object dictionary

        Returns:
            Processed data object with updated semantic state
        """
        processed = self.runtime.process_data(data_object)
        self.data_registry[processed['data_id']] = processed
        return processed

    def batch_ingest(self, data_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ingest and process a batch of data objects.

        Args:
            data_objects: List of data object dicts

        Returns:
            List of processed data objects
        """
        processed_list = self.runtime.batch_process(data_objects)
        for obj in processed_list:
            self.data_registry[obj['data_id']] = obj
        return processed_list

    def get_data(self, data_id: str) -> Dict[str, Any]:
        """
        Retrieve the current state of a registered data object.

        Args:
            data_id: Unique identifier for the data object

        Returns:
            Current state of the data object
        """
        return self.data_registry.get(data_id, {})

    def monitor_entropy(self, data_id: str) -> float:
        """
        Retrieve the current entropy level of a data object.

        Args:
            data_id: Unique identifier for the data object

        Returns:
            Current entropy level (0-1)
        """
        data = self.get_data(data_id)
        return data.get('entropy_level', 0.0)

    def is_authorized(self, data_id: str) -> bool:
        """
        Check if a data object is currently in an authorized semantic state.

        Args:
            data_id: Unique identifier for the data object

        Returns:
            True if resolution_state is 'authorized', False otherwise
        """
        data = self.get_data(data_id)
        return data.get('resolution_state') == 'authorized'

    def update_context(self, data_id: str, new_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the context vector of a data object and re-process.

        Args:
            data_id: Unique identifier for the data object
            new_context: New context vector dictionary

        Returns:
            Updated data object
        """
        data = self.get_data(data_id)
        if not data:
            raise ValueError(f"Data object {data_id} not found.")

        data['context_vector'] = new_context
        return self.ingest(data)
