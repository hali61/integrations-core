# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
from copy import deepcopy

CHECK_NAME = 'scylla'
NAMESPACE = 'scylla.'

base_metric_group_map = {
    'scylla.alien': [
        'scylla.alien.receive_batch_queue_length',
        'scylla.alien.total_received_messages',
        'scylla.alien.total_sent_messages',
    ],
    'scylla.batchlog_manager': [
        'scylla.batchlog_manager.total_write_replay_attempts',
    ],
    'scylla.cache': [
        'scylla.cache.active_reads',
        'scylla.cache.bytes_total',
        'scylla.cache.bytes_used',
        'scylla.cache.concurrent_misses_same_key',
        'scylla.cache.mispopulations',
        'scylla.cache.partition_evictions',
        'scylla.cache.partition_hits',
        'scylla.cache.partition_insertions',
        'scylla.cache.partition_merges',
        'scylla.cache.partition_misses',
        'scylla.cache.partition_removals',
        'scylla.cache.partitions',
        'scylla.cache.pinned_dirty_memory_overload',
        'scylla.cache.reads',
        'scylla.cache.reads_with_misses',
        'scylla.cache.row_evictions',
        'scylla.cache.row_hits',
        'scylla.cache.row_insertions',
        'scylla.cache.row_misses',
        'scylla.cache.row_removals',
        'scylla.cache.rows',
        'scylla.cache.rows_dropped_from_memtable',
        'scylla.cache.rows_merged_from_memtable',
        'scylla.cache.rows_processed_from_memtable',
        'scylla.cache.sstable_partition_skips',
        'scylla.cache.sstable_reader_recreations',
        'scylla.cache.sstable_row_skips',
        'scylla.cache.static_row_insertions',
    ],
    'scylla.commitlog': [
        'scylla.commitlog.alloc',
        'scylla.commitlog.allocating_segments',
        'scylla.commitlog.bytes_written',
        'scylla.commitlog.cycle',
        'scylla.commitlog.disk_total_bytes',
        'scylla.commitlog.flush',
        'scylla.commitlog.flush_limit_exceeded',
        'scylla.commitlog.memory_buffer_bytes',
        'scylla.commitlog.pending_allocations',
        'scylla.commitlog.pending_flushes',
        'scylla.commitlog.requests_blocked_memory',
        'scylla.commitlog.segments',
        'scylla.commitlog.slack',
        'scylla.commitlog.unused_segments',
    ],
    'scylla.compaction_manager': [
        'scylla.compaction_manager.compactions',
    ],
    'scylla.cql': [
        'scylla.cql.authorized_prepared_statements_cache_evictions',
        'scylla.cql.authorized_prepared_statements_cache_size',
        'scylla.cql.batches',
        'scylla.cql.batches_pure_logged',
        'scylla.cql.batches_pure_unlogged',
        'scylla.cql.batches_unlogged_from_logged',
        'scylla.cql.deletes',
        'scylla.cql.filtered_read_requests',
        'scylla.cql.filtered_rows_dropped_total',
        'scylla.cql.filtered_rows_matched_total',
        'scylla.cql.filtered_rows_read_total',
        'scylla.cql.inserts',
        'scylla.cql.prepared_cache_evictions',
        'scylla.cql.prepared_cache_memory_footprint',
        'scylla.cql.prepared_cache_size',
        'scylla.cql.reads',
        'scylla.cql.reverse_queries',
        'scylla.cql.rows_read',
        'scylla.cql.secondary_index_creates',
        'scylla.cql.secondary_index_drops',
        'scylla.cql.secondary_index_reads',
        'scylla.cql.secondary_index_rows_read',
        'scylla.cql.statements_in_batches',
        'scylla.cql.unpaged_select_queries',
        'scylla.cql.updates',
        'scylla.cql.user_prepared_auth_cache_footprint',
    ],
    'scylla.database': [
        'scylla.database.active_reads',
        'scylla.database.active_reads_memory_consumption',
        'scylla.database.clustering_filter_count',
        'scylla.database.clustering_filter_fast_path_count',
        'scylla.database.clustering_filter_sstables_checked',
        'scylla.database.clustering_filter_surviving_sstables',
        'scylla.database.counter_cell_lock_acquisition',
        'scylla.database.counter_cell_lock_pending',
        'scylla.database.dropped_view_updates',
        'scylla.database.large_partition_exceeding_threshold',
        'scylla.database.multishard_query_failed_reader_saves',
        'scylla.database.multishard_query_failed_reader_stops',
        'scylla.database.multishard_query_unpopped_bytes',
        'scylla.database.multishard_query_unpopped_fragments',
        'scylla.database.paused_reads',
        'scylla.database.paused_reads_permit_based_evictions',
        'scylla.database.querier_cache_drops',
        'scylla.database.querier_cache_lookups',
        'scylla.database.querier_cache_memory_based_evictions',
        'scylla.database.querier_cache_misses',
        'scylla.database.querier_cache_population',
        'scylla.database.querier_cache_resource_based_evictions',
        'scylla.database.querier_cache_time_based_evictions',
        'scylla.database.queued_reads',
        'scylla.database.requests_blocked_memory',
        'scylla.database.requests_blocked_memory_current',
        'scylla.database.short_data_queries',
        'scylla.database.short_mutation_queries',
        'scylla.database.sstable_read_queue_overloads',
        'scylla.database.total_reads',
        'scylla.database.total_reads_failed',
        'scylla.database.total_result_bytes',
        'scylla.database.total_view_updates_failed_local',
        'scylla.database.total_view_updates_failed_remote',
        'scylla.database.total_view_updates_pushed_local',
        'scylla.database.total_view_updates_pushed_remote',
        'scylla.database.total_writes',
        'scylla.database.total_writes_failed',
        'scylla.database.total_writes_timedout',
        'scylla.database.view_building_paused',
        'scylla.database.view_update_backlog',
    ],
    'scylla.execution_stages': [
        'scylla.execution_stages.function_calls_enqueued',
        'scylla.execution_stages.function_calls_executed',
        'scylla.execution_stages.tasks_preempted',
        'scylla.execution_stages.tasks_scheduled',
    ],
    'scylla.gossip': [
        'scylla.gossip.heart_beat',
    ],
    'scylla.hints': [
        'scylla.hints.for_views_manager_corrupted_files',
        'scylla.hints.for_views_manager_discarded',
        'scylla.hints.for_views_manager_dropped',
        'scylla.hints.for_views_manager_errors',
        'scylla.hints.for_views_manager_sent',
        'scylla.hints.for_views_manager_size_of_hints_in_progress',
        'scylla.hints.for_views_manager_written',
        'scylla.hints.manager_corrupted_files',
        'scylla.hints.manager_discarded',
        'scylla.hints.manager_dropped',
        'scylla.hints.manager_errors',
        'scylla.hints.manager_sent',
        'scylla.hints.manager_size_of_hints_in_progress',
        'scylla.hints.manager_written',
    ],
    'scylla.httpd': [
        'scylla.httpd.connections_current',
        'scylla.httpd.connections_total',
        'scylla.httpd.read_errors',
        'scylla.httpd.reply_errors',
        'scylla.httpd.requests_served',
    ],
    'scylla.io_queue': [
        'scylla.io_queue.delay',
        'scylla.io_queue.queue_length',
        'scylla.io_queue.shares',
        'scylla.io_queue.total_bytes',
        'scylla.io_queue.total_operations',
    ],
    'scylla.lsa': [
        'scylla.lsa.free_space',
        'scylla.lsa.large_objects_total_space_bytes',
        'scylla.lsa.memory_allocated',
        'scylla.lsa.memory_compacted',
        'scylla.lsa.non_lsa_used_space_bytes',
        'scylla.lsa.occupancy',
        'scylla.lsa.segments_compacted',
        'scylla.lsa.segments_migrated',
        'scylla.lsa.small_objects_total_space_bytes',
        'scylla.lsa.small_objects_used_space_bytes',
        'scylla.lsa.total_space_bytes',
        'scylla.lsa.used_space_bytes',
    ],
    'scylla.memory': [
        'scylla.memory.allocated_memory',
        'scylla.memory.cross_cpu_free_operations',
        'scylla.memory.dirty_bytes',
        'scylla.memory.free_memory',
        'scylla.memory.free_operations',
        'scylla.memory.malloc_live_objects',
        'scylla.memory.malloc_operations',
        'scylla.memory.reclaims_operations',
        'scylla.memory.regular_dirty_bytes',
        'scylla.memory.regular_virtual_dirty_bytes',
        'scylla.memory.streaming_dirty_bytes',
        'scylla.memory.streaming_virtual_dirty_bytes',
        'scylla.memory.system_dirty_bytes',
        'scylla.memory.system_virtual_dirty_bytes',
        'scylla.memory.total_memory',
        'scylla.memory.virtual_dirty_bytes',
    ],
    'scylla.memtables': [
        'scylla.memtables.pending_flushes',
        'scylla.memtables.pending_flushes_bytes',
    ],
    'scylla.node': ['scylla.node.operation_mode'],
    'scylla.query_processor': [
        'scylla.query_processor.queries',
        'scylla.query_processor.statements_prepared',
    ],
    'scylla.reactor': [
        'scylla.reactor.aio_bytes_read',
        'scylla.reactor.aio_bytes_write',
        'scylla.reactor.aio_errors',
        'scylla.reactor.aio_reads',
        'scylla.reactor.aio_writes',
        'scylla.reactor.cpp_exceptions',
        'scylla.reactor.cpu_busy_ms',
        'scylla.reactor.cpu_steal_time_ms',
        'scylla.reactor.fstream_read_bytes',
        'scylla.reactor.fstream_read_bytes_blocked',
        'scylla.reactor.fstream_reads',
        'scylla.reactor.fstream_reads_ahead_bytes_discarded',
        'scylla.reactor.fstream_reads_aheads_discarded',
        'scylla.reactor.fstream_reads_blocked',
        'scylla.reactor.fsyncs',
        'scylla.reactor.io_queue_requests',
        'scylla.reactor.io_threaded_fallbacks',
        'scylla.reactor.logging_failures',
        'scylla.reactor.polls',
        'scylla.reactor.tasks_pending',
        'scylla.reactor.tasks_processed',
        'scylla.reactor.timers_pending',
        'scylla.reactor.utilization',
    ],
    'scylla.scheduler': [
        'scylla.scheduler.queue_length',
        'scylla.scheduler.runtime_ms',
        'scylla.scheduler.shares',
        'scylla.scheduler.tasks_processed',
        'scylla.scheduler.time_spent_on_task_quota_violations_ms',
    ],
    'scylla.sstables': [
        'scylla.sstables.capped_local_deletion_time',
        'scylla.sstables.capped_tombstone_deletion_time',
        'scylla.sstables.cell_tombstone_writes',
        'scylla.sstables.cell_writes',
        'scylla.sstables.index_page_blocks',
        'scylla.sstables.index_page_hits',
        'scylla.sstables.index_page_misses',
        'scylla.sstables.partition_reads',
        'scylla.sstables.partition_seeks',
        'scylla.sstables.partition_writes',
        'scylla.sstables.range_partition_reads',
        'scylla.sstables.range_tombstone_writes',
        'scylla.sstables.row_reads',
        'scylla.sstables.row_writes',
        'scylla.sstables.single_partition_reads',
        'scylla.sstables.sstable_partition_reads',
        'scylla.sstables.static_row_writes',
        'scylla.sstables.tombstone_writes',
    ],
    'scylla.storage': [
        'scylla.storage.proxy.coordinator_background_read_repairs',
        'scylla.storage.proxy.coordinator_background_reads',
        'scylla.storage.proxy.coordinator_background_replica_writes_failed_local_node',
        'scylla.storage.proxy.coordinator_background_write_bytes',
        'scylla.storage.proxy.coordinator_background_writes',
        'scylla.storage.proxy.coordinator_background_writes_failed',
        'scylla.storage.proxy.coordinator_canceled_read_repairs',
        'scylla.storage.proxy.coordinator_completed_reads_local_node',
        'scylla.storage.proxy.coordinator_current_throttled_base_writes',
        'scylla.storage.proxy.coordinator_current_throttled_writes',
        'scylla.storage.proxy.coordinator_foreground_read_repair',
        'scylla.storage.proxy.coordinator_foreground_reads',
        'scylla.storage.proxy.coordinator_foreground_writes',
        'scylla.storage.proxy.coordinator_last_mv_flow_control_delay',
        'scylla.storage.proxy.coordinator_queued_write_bytes',
        'scylla.storage.proxy.coordinator_range_timeouts',
        'scylla.storage.proxy.coordinator_range_unavailable',
        'scylla.storage.proxy.coordinator_read_errors_local_node',
        'scylla.storage.proxy.coordinator_read_latency.count',
        'scylla.storage.proxy.coordinator_read_latency.sum',
        'scylla.storage.proxy.coordinator_read_repair_write_attempts_local_node',
        'scylla.storage.proxy.coordinator_read_retries',
        'scylla.storage.proxy.coordinator_read_timeouts',
        'scylla.storage.proxy.coordinator_read_unavailable',
        'scylla.storage.proxy.coordinator_reads_local_node',
        'scylla.storage.proxy.coordinator_speculative_data_reads',
        'scylla.storage.proxy.coordinator_speculative_digest_reads',
        'scylla.storage.proxy.coordinator_throttled_writes',
        'scylla.storage.proxy.coordinator_total_write_attempts_local_node',
        'scylla.storage.proxy.coordinator_write_errors_local_node',
        'scylla.storage.proxy.coordinator_write_latency.count',
        'scylla.storage.proxy.coordinator_write_latency.sum',
        'scylla.storage.proxy.coordinator_write_timeouts',
        'scylla.storage.proxy.coordinator_write_unavailable',
        'scylla.storage.proxy.replica_cross_shard_ops',
        'scylla.storage.proxy.replica_forwarded_mutations',
        'scylla.storage.proxy.replica_forwarding_errors',
        'scylla.storage.proxy.replica_reads',
        'scylla.storage.proxy.replica_received_counter_updates',
        'scylla.storage.proxy.replica_received_mutations',
    ],
    'scylla.streaming': [
        'scylla.streaming.total_incoming_bytes',
        'scylla.streaming.total_outgoing_bytes',
    ],
    'scylla.thrift': [
        'scylla.thrift.current_connections',
        'scylla.thrift.served',
        'scylla.thrift.thrift_connections',
    ],
    'scylla.tracing': [
        'scylla.tracing.active_sessions',
        'scylla.tracing.cached_records',
        'scylla.tracing.dropped_records',
        'scylla.tracing.dropped_sessions',
        'scylla.tracing.flushing_records',
        'scylla.tracing.keyspace_helper_bad_column_family_errors',
        'scylla.tracing.keyspace_helper_tracing_errors',
        'scylla.tracing.pending_for_write_records',
        'scylla.tracing.trace_errors',
        'scylla.tracing.trace_records_count',
    ],
    'scylla.transport': [
        'scylla.transport.cql_connections',
        'scylla.transport.current_connections',
        'scylla.transport.requests_blocked_memory',
        'scylla.transport.requests_blocked_memory_current',
        'scylla.transport.requests_served',
        'scylla.transport.requests_serving',
    ],
}

new_metrics_version_3_2 = {
    'scylla.storage': [
        'scylla.storage.proxy.coordinator_cas_read_contention.count',
        'scylla.storage.proxy.coordinator_cas_read_contention.sum',
        'scylla.storage.proxy.coordinator_cas_read_latency.count',
        'scylla.storage.proxy.coordinator_cas_read_latency.sum',
        'scylla.storage.proxy.coordinator_cas_read_timouts',
        'scylla.storage.proxy.coordinator_cas_read_unavailable',
        'scylla.storage.proxy.coordinator_cas_read_unfinished_commit',
        'scylla.storage.proxy.coordinator_cas_write_condition_not_met',
        'scylla.storage.proxy.coordinator_cas_write_contention.count',
        'scylla.storage.proxy.coordinator_cas_write_contention.sum',
        'scylla.storage.proxy.coordinator_cas_write_latency.count',
        'scylla.storage.proxy.coordinator_cas_write_latency.sum',
        'scylla.storage.proxy.coordinator_cas_write_timeouts',
        'scylla.storage.proxy.coordinator_cas_write_unavailable',
        'scylla.storage.proxy.coordinator_cas_write_unfinished_commit',
        'scylla.storage.proxy.coordinator_reads_coordinator_outside_replica_set',
        'scylla.storage.proxy.coordinator_writes_coordinator_outside_replica_set',
    ],
    'scylla.transport': [
        'scylla.transport.requests_memory_available',
    ],
}

new_metrics_version_3_3 = {
    'scylla.reactor': [
        'scylla.reactor.abandoned_failed_futures',
    ]
}

new_metrics_version_5 = {
    'scylla.cache': [
        'scylla.cache.dummy_row_hits',
        'scylla.cache.range_tombstone_reads',
        'scylla.cache.row_tombstone_reads',
        'scylla.cache.rows_compacted_with_tombstones',
        'scylla.cache.rows_dropped_by_tombstones',
    ],
    'scylla.cdc': [
        'scylla.cdc.operations_failed',
        'scylla.cdc.operations_on_clustering_row_performed_failed',
        'scylla.cdc.operations_on_clustering_row_performed_total',
        'scylla.cdc.operations_on_list_performed_failed',
        'scylla.cdc.operations_on_list_performed_total',
        'scylla.cdc.operations_on_map_performed_failed',
        'scylla.cdc.operations_on_map_performed_total',
        'scylla.cdc.operations_on_partition_delete_performed_failed',
        'scylla.cdc.operations_on_partition_delete_performed_total',
        'scylla.cdc.operations_on_range_tombstone_performed_failed',
        'scylla.cdc.operations_on_range_tombstone_performed_total',
        'scylla.cdc.operations_on_row_delete_performed_failed',
        'scylla.cdc.operations_on_row_delete_performed_total',
        'scylla.cdc.operations_on_set_performed_failed',
        'scylla.cdc.operations_on_set_performed_total',
        'scylla.cdc.operations_on_static_row_performed_failed',
        'scylla.cdc.operations_on_static_row_performed_total',
        'scylla.cdc.operations_on_udt_performed_failed',
        'scylla.cdc.operations_on_udt_performed_total',
        'scylla.cdc.operations_total',
        'scylla.cdc.operations_with_postimage_failed',
        'scylla.cdc.operations_with_postimage_total',
        'scylla.cdc.operations_with_preimage_failed',
        'scylla.cdc.operations_with_preimage_total',
        'scylla.cdc.preimage_selects_failed',
        'scylla.cdc.preimage_selects_total',
    ],
    'scylla.commitlog': [
        'scylla.commitlog.active_allocations',
        'scylla.commitlog.blocked_on_new_segment',
        'scylla.commitlog.bytes_flush_requested',
        'scylla.commitlog.bytes_released',
        'scylla.commitlog.disk_active_bytes',
        'scylla.commitlog.disk_slack_end_bytes',
    ],
    'scylla.compaction_manager': [
        'scylla.compaction_manager.backlog',
        'scylla.compaction_manager.completed_compactions',
        'scylla.compaction_manager.failed_compactions',
        'scylla.compaction_manager.normalized_backlog',
        'scylla.compaction_manager.pending_compactions',
        'scylla.compaction_manager.postponed_compactions',
        'scylla.compaction_manager.validation_errors',
    ],
    'scylla.cql': [
        'scylla.cql.deletes_per_ks',
        'scylla.cql.inserts_per_ks',
        'scylla.cql.reads_per_ks',
        'scylla.cql.select_allow_filtering',
        'scylla.cql.select_bypass_caches',
        'scylla.cql.select_parallelized',
        'scylla.cql.select_partition_range_scan',
        'scylla.cql.select_partition_range_scan_no_bypass_cache',
        'scylla.cql.unpaged_select_queries_per_ks',
        'scylla.cql.unprivileged_entries_evictions_on_size',
        'scylla.cql.updates_per_ks',
    ],
    'scylla.database': [
        'scylla.database.disk_reads',
        'scylla.database.reads_rate_limited',
        'scylla.database.reads_shed_due_to_overload',
        'scylla.database.schema_changed',
        'scylla.database.sstable_read',
        'scylla.database.writes_rate_limited',
    ],
    'scylla.forward_service': [
        'scylla.forward_service.requests_dispatched_to_other_nodes',
        'scylla.forward_service.requests_dispatched_to_own_shards',
        'scylla.forward_service.requests_executed',
    ],
    'scylla.gossip': [
        'scylla.gossip.live',
        'scylla.gossip.unreachable',
    ],
    'scylla.hints': [
        'scylla.hints.for_views_manager_pending_drains',
        'scylla.hints.for_views_manager_pending_sends',
        'scylla.hints.manager_pending_drains',
        'scylla.hints.manager_pending_sends',
    ],
    'scylla.io_queue': [
        'scylla.io_queue.adjusted_consumption',
        'scylla.io_queue.consumption',
        'scylla.io_queue.disk_queue_length',
        'scylla.io_queue.read_ops',
        'scylla.io_queue.starvation_time_sec',
        'scylla.io_queue.total_delay_sec',
        'scylla.io_queue.total_exec_sec',
        'scylla.io_queue.total_read_bytes',
        'scylla.io_queue.total_split_bytes',
        'scylla.io_queue.total_split_ops',
        'scylla.io_queue.write_bytes',
        'scylla.io_queue.write_ops',
    ],
    'scylla.lsa': [
        'scylla.lsa.memory_evicted',
        'scylla.lsa.memory_freed',
    ],
    'scylla.memory': [
        'scylla.memory.malloc_failed',
    ],
    'scylla.memtables': [
        'scylla.memtables.failed_flushes',
    ],
    'scylla.node': [
        'scylla.node.ops_finished_percentage',
    ],
    'scylla.per_partition': [
        'scylla.per_partition.rate_limiter_allocations',
        'scylla.per_partition.rate_limiter_failed_allocations',
        'scylla.per_partition.rate_limiter_load_factor',
        'scylla.per_partition.rate_limiter_probe_count',
        'scylla.per_partition.rate_limiter_successful_lookups',
    ],
    'scylla.raft': [
        'scylla.raft.add_entries',
        'scylla.raft.applied_entries',
        'scylla.raft.group0_status',
        'scylla.raft.in_memory_log_size',
        'scylla.raft.messages_received',
        'scylla.raft.messages_sent',
        'scylla.raft.persisted_log_entriespersisted_log_entries',
        'scylla.raft.polls',
        'scylla.raft.queue_entries_for_apply',
        'scylla.raft.sm_load_snapshot',
        'scylla.raft.snapshots_taken',
        'scylla.raft.store_snapshot',
        'scylla.raft.store_term_and_vote',
        'scylla.raft.truncate_persisted_log',
        'scylla.raft.waiter_awaiken',
        'scylla.raft.waiter_dropped',
    ],
    'scylla.reactor': [
        'scylla.reactor.abandoned_failed_futures',
        'scylla.reactor.aio_outsizes',
    ],
    'scylla.repair': [
        'scylla.repair.row_from_disk_nr',
        'scylla.repair.rx_hashes_nr',
        'scylla.repair.rx_row_bytes',
        'scylla.repair.rx_row_nr',
        'scylla.repair.tx_hashes_nr',
        'scylla.repair.tx_row_bytes',
        'scylla.repair.tx_row_nr',
    ],
    'scylla.schema_commitlog': [
        'scylla.schema_commitlog.active_allocations',
        'scylla.schema_commitlog.alloc',
        'scylla.schema_commitlog.allocating_segments',
        'scylla.schema_commitlog.blocked_on_new_segment',
        'scylla.schema_commitlog.bytes_flush_requested',
        'scylla.schema_commitlog.bytes_released',
        'scylla.schema_commitlog.bytes_written',
        'scylla.schema_commitlog.cycle',
        'scylla.schema_commitlog.disk_active_bytes',
        'scylla.schema_commitlog.disk_slack_end_bytes',
        'scylla.schema_commitlog.disk_total_bytes',
        'scylla.schema_commitlog.flush',
        'scylla.schema_commitlog.flush_limit_exceeded',
        'scylla.schema_commitlog.memory_buffer_bytes',
        'scylla.schema_commitlog.pending_allocations',
        'scylla.schema_commitlog.pending_flushes',
        'scylla.schema_commitlog.requests_blocked_memory',
        'scylla.schema_commitlog.segments',
        'scylla.schema_commitlog.slack',
        'scylla.schema_commitlog.unused_segments',
    ],
    'scylla.scheduler': [
        'scylla.scheduler.starvetime_ms',
        'scylla.scheduler.waittime_ms',
    ],
    'scylla.sstables': [
        'scylla.sstables.bloom_filter_memory_size',
        'scylla.sstables.currently_open_for_reading',
        'scylla.sstables.currently_open_for_writing',
        'scylla.sstables.index_page_cache_bytes',
        'scylla.sstables.index_page_cache_bytes_in_std',
        'scylla.sstables.index_page_cache_evictions',
        'scylla.sstables.index_page_cache_hits',
        'scylla.sstables.index_page_cache_misses',
        'scylla.sstables.index_page_cache_populations',
        'scylla.sstables.index_page_evictions',
        'scylla.sstables.index_page_populations',
        'scylla.sstables.index_page_used_bytes',
        'scylla.sstables.pi_auto_scale_events',
        'scylla.sstables.pi_cache_block_count',
        'scylla.sstables.pi_cache_bytes',
        'scylla.sstables.pi_cache_evictions',
        'scylla.sstables.pi_cache_hits_l0',
        'scylla.sstables.pi_cache_hits_l1',
        'scylla.sstables.pi_cache_hits_l2',
        'scylla.sstables.pi_cache_misses_l0',
        'scylla.sstables.pi_cache_misses_l1',
        'scylla.sstables.pi_cache_misses_l2',
        'scylla.sstables.pi_cache_populations',
        'scylla.sstables.range_tombstone_reads',
        'scylla.sstables.row_tombstone_reads',
        'scylla.sstables.total_deleted',
        'scylla.sstables.total_open_for_reading',
        'scylla.sstables.total_open_for_writing',
    ],
    'scylla.storage': [
        'scylla.storage.proxy.coordinator_cas_background',
        'scylla.storage.proxy.coordinator_cas_foreground',
        'scylla.storage.proxy.coordinator_cas_prune',
        'scylla.storage.proxy.coordinator_read_latency_summary.count',
        'scylla.storage.proxy.coordinator_read_latency_summary.quantile',
        'scylla.storage.proxy.coordinator_write_latency_summary.count',
        'scylla.storage.proxy.coordinator_write_latency_summary.quantile',
    ],
    'scylla.streaming': [
        'scylla.streaming.finished_percentage',
    ],
    'scylla.stall': ['scylla.stall.detector_reported'],
    'scylla.transport': [
        'scylla.transport.auth_responses',
        'scylla.transport.cql_errors_total',
        'scylla.transport.execute_requests',
        'scylla.transport.options_requests',
        'scylla.transport.prepare_requests',
        'scylla.transport.query_requests',
        'scylla.transport.register_requests',
        'scylla.transport.requests_memory_available',
        'scylla.transport.requests_shed',
        'scylla.transport.startups',
    ],
    'scylla.view': [
        'scylla.view.builder_builds_in_progress',
        'scylla.view.builder_pending_bookkeeping_ops',
        'scylla.view.builder_steps_failed',
        'scylla.view.builder_steps_performed',
        'scylla.view.update_generator_pending_registrations',
        'scylla.view.update_generator_queued_batches_count',
        'scylla.view.update_generator_sstables_pending_work',
        'scylla.view.update_generator_sstables_to_move_count',
    ],
}

changed_or_removed_metrics_ver_5 = {
    'scylla.database': [
        'scylla.database.querier_cache_memory_based_evictions',
    ],
    'scylla.lsa': [
        'scylla.lsa.segments_migrated',
    ],
    'scylla.reactor': [
        'scylla.reactor.io_queue_requests',
    ],
    'scylla.sstables': [
        'scylla.sstables.sstable_partition_reads',
    ],
    'scylla.storage': [
        'scylla.storage.proxy.coordinator_background_read_repairs',
        'scylla.storage.proxy.coordinator_background_write_bytes',
        'scylla.storage.proxy.coordinator_background_writes_failed',
        'scylla.storage.proxy.coordinator_canceled_read_repairs',
        'scylla.storage.proxy.coordinator_foreground_read_repair',
        'scylla.storage.proxy.coordinator_queued_write_bytes',
        'scylla.storage.proxy.coordinator_range_timeouts',
        'scylla.storage.proxy.coordinator_range_unavailable',
        'scylla.storage.proxy.coordinator_read_retries',
        'scylla.storage.proxy.coordinator_read_timeouts',
        'scylla.storage.proxy.coordinator_read_unavailable',
        'scylla.storage.proxy.coordinator_speculative_data_reads',
        'scylla.storage.proxy.coordinator_speculative_digest_reads',
        'scylla.storage.proxy.coordinator_throttled_writes',
        'scylla.storage.proxy.coordinator_write_timeouts',
        'scylla.storage.proxy.coordinator_write_unavailable',
        'scylla.storage.proxy.replica_forwarded_mutations',
        'scylla.storage.proxy.replica_forwarding_errors',
        'scylla.storage.proxy.replica_reads',
        'scylla.storage.proxy.replica_received_counter_updates',
        'scylla.storage.proxy.replica_received_mutations',
    ],
    'scylla.thrift': [
        'scylla.thrift.current_connections',
        'scylla.thrift.served',
        'scylla.thrift.thrift_connections',
    ],
}
# fmt: on


def modify_metrics_map(base_map, map_to_add, map_to_delete=None):
    for key, value in map_to_add.items():
        if key in base_map:
            base_map[key].extend(value)
        else:
            base_map[key] = value

    if map_to_delete:
        for key, values in map_to_delete.items():
            if key in base_map:
                base_map[key] = [v for v in base_map[key] if v not in values]

    return base_map


instance_3_2_metric_group_map = modify_metrics_map(deepcopy(base_metric_group_map), new_metrics_version_3_2)

instance_3_3_metric_group_map = modify_metrics_map(deepcopy(instance_3_2_metric_group_map), new_metrics_version_3_3)

instance_5_2_metric_group_map = modify_metrics_map(
    deepcopy(base_metric_group_map), new_metrics_version_5, changed_or_removed_metrics_ver_5
)


FLAKY_METRICS_3 = [
    'scylla.reactor.abandoned_failed_futures',
    'scylla.storage.proxy.coordinator_cas_read_contention.count',
    'scylla.storage.proxy.coordinator_cas_read_contention.sum',
    'scylla.storage.proxy.coordinator_cas_read_latency.count',
    'scylla.storage.proxy.coordinator_cas_read_latency.sum',
    'scylla.storage.proxy.coordinator_cas_read_timouts',
    'scylla.storage.proxy.coordinator_cas_read_unavailable',
    'scylla.storage.proxy.coordinator_cas_read_unfinished_commit',
    'scylla.storage.proxy.coordinator_cas_write_condition_not_met',
    'scylla.storage.proxy.coordinator_cas_write_contention.count',
    'scylla.storage.proxy.coordinator_cas_write_contention.sum',
    'scylla.storage.proxy.coordinator_cas_write_latency.count',
    'scylla.storage.proxy.coordinator_cas_write_latency.sum',
    'scylla.storage.proxy.coordinator_cas_write_timeouts',
    'scylla.storage.proxy.coordinator_cas_write_unavailable',
    'scylla.storage.proxy.coordinator_cas_write_unfinished_commit',
    'scylla.storage.proxy.coordinator_reads_coordinator_outside_replica_set',
    'scylla.storage.proxy.coordinator_writes_coordinator_outside_replica_set',
    'scylla.transport.requests_memory_available',
]

FLAKY_METRICS_5 = [
    'scylla.memory.streaming_dirty_bytes',
    'scylla.memory.streaming_virtual_dirty_bytes',
    'scylla.raft.add_entries',
    'scylla.raft.applied_entries',
    'scylla.raft.in_memory_log_size',
    'scylla.raft.messages_received',
    'scylla.raft.messages_sent',
    'scylla.raft.persisted_log_entriespersisted_log_entries',
    'scylla.raft.polls',
    'scylla.raft.queue_entries_for_apply',
    'scylla.raft.sm_load_snapshot',
    'scylla.raft.snapshots_taken',
    'scylla.raft.store_snapshot',
    'scylla.raft.store_term_and_vote',
    'scylla.raft.truncate_persisted_log',
    'scylla.raft.waiter_awaiken',
    'scylla.raft.waiter_dropped',
    'scylla.repair.row_from_disk_nr',
    'scylla.repair.rx_hashes_nr',
    'scylla.repair.rx_row_bytes',
    'scylla.repair.rx_row_nr',
    'scylla.repair.tx_hashes_nr',
    'scylla.repair.tx_row_bytes',
    'scylla.repair.tx_row_nr',
    'scylla.schema_commitlog.active_allocations',
    'scylla.schema_commitlog.alloc',
    'scylla.schema_commitlog.allocating_segments',
    'scylla.schema_commitlog.blocked_on_new_segment',
    'scylla.schema_commitlog.bytes_flush_requested',
    'scylla.schema_commitlog.bytes_released',
    'scylla.schema_commitlog.bytes_written',
    'scylla.schema_commitlog.cycle',
    'scylla.schema_commitlog.disk_active_bytes',
    'scylla.schema_commitlog.disk_slack_end_bytes',
    'scylla.schema_commitlog.disk_total_bytes',
    'scylla.schema_commitlog.flush',
    'scylla.schema_commitlog.flush_limit_exceeded',
    'scylla.schema_commitlog.memory_buffer_bytes',
    'scylla.schema_commitlog.pending_allocations',
    'scylla.schema_commitlog.pending_flushes',
    'scylla.schema_commitlog.requests_blocked_memory',
    'scylla.schema_commitlog.segments',
    'scylla.schema_commitlog.slack',
    'scylla.schema_commitlog.unused_segments',
    'scylla.view.builder_pending_bookkeeping_ops',
    'scylla_forward_service_requests_dispatched_to_other_nodes',
    'scylla_forward_service_requests_dispatched_to_own_shards',
    'scylla_forward_service_requests_executed',
]

INSTANCE_DEFAULT_GROUPS = [
    'scylla.cache',
    'scylla.compaction_manager',
    'scylla.gossip',
    'scylla.node',
    'scylla.reactor',
    'scylla.storage',
    'scylla.streaming',
    'scylla.transport',
]

# Additional groups exposed in all environments
base_additional_groups = [
    'scylla.alien',
    'scylla.batchlog_manager',
    'scylla.commitlog',
    'scylla.cql',
    'scylla.database',
    'scylla.execution_stages',
    'scylla.hints',
    'scylla.httpd',
    'scylla.io_queue',
    'scylla.lsa',
    'scylla.memory',
    'scylla.memtables',
    'scylla.query_processor',
    'scylla.scheduler',
    'scylla.sstables',
    'scylla.tracing',
]

# Additional groups exposed in 3.* environments
instance_3_additional_groups = [
    'scylla.thrift',
]

# Additional groups exposed in 5.* environments
instance_5_additional_groups = [
    'scylla.cdc',
    'scylla.forward_service',
    'scylla.raft',
    'scylla.repair',
    'scylla.schema_commitlog',
    'scylla.stall',
    'scylla.view',
]

instance_3_groups = base_additional_groups + instance_3_additional_groups
instance_5_groups = base_additional_groups + instance_5_additional_groups

MAP_VERSION_TO_METRICS = {
    '3.1.2': base_metric_group_map,
    '3.2.1': instance_3_2_metric_group_map,
    '3.3.1': instance_3_3_metric_group_map,
    '5.2.6': instance_5_2_metric_group_map,
}
# fmt: on

# expand the lists into a single list of metrics
def get_metrics(metric_groups):
    """Given a list of metric groups, return single consolidated list"""
    return sorted(m for g in metric_groups for m in MAP_VERSION_TO_METRICS[os.environ['SCYLLA_VERSION']][g])


INSTANCE_DEFAULT_METRICS = get_metrics(INSTANCE_DEFAULT_GROUPS)
if os.environ['SCYLLA_VERSION'] == '5.2.6':
    INSTANCE_ADDITIONAL_GROUPS = instance_5_groups
    INSTANCE_ADDITIONAL_METRICS = get_metrics(instance_5_groups)
    FLAKY_METRICS = FLAKY_METRICS_5
else:
    INSTANCE_ADDITIONAL_GROUPS = instance_3_groups
    INSTANCE_ADDITIONAL_METRICS = get_metrics(instance_3_groups)
    FLAKY_METRICS = FLAKY_METRICS_3
