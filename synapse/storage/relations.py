# -*- coding: utf-8 -*-
# Copyright 2019 New Vector Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import attr

from synapse.storage._base import SQLBaseStore

logger = logging.getLogger(__name__)


@attr.s
class PaginationChunk(object):
    chunk = attr.ib()
    limited = attr.ib()
    next_batch = attr.ib(default=None)
    prev_batch = attr.ib(default=None)

    def to_dict(self):
        return attr.asdict(self)


class RelationsStore(SQLBaseStore):
    def get_recent_relations_for_event(
        self, event_id, relation_type=None, event_type=None, limit=5
    ):
        """
        """

        # TODO: Pagination tokens

        where_clause = ["relates_to_id = ?"]
        where_args = [event_id]

        if relation_type:
            where_clause.append("relation_type = ?")
            where_args.append(relation_type)

        if event_type:
            where_clause.append("type = ?")
            where_args.append(event_type)

        sql = """
            SELECT event_id FROM event_relations
            INNER JOIN events USING (event_id)
            WHERE %s
            ORDER BY topological_ordering DESC, stream_ordering DESC
            LIMIT ?
        """ % (
            " AND ".join(where_clause),
        )

        def _get_recent_references_for_event_txn(txn):
            txn.execute(sql, where_args + [limit + 1])

            events = [row[0] for row in txn]

            return PaginationChunk(
                chunk=list(events[:limit]), limited=len(events) > limit
            )

        return self.runInteraction(
            "get_recent_references_for_event", _get_recent_references_for_event_txn
        )
