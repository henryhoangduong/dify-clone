import json
import pickle
from json import JSONDecodeError

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from extensions.ext_database import db
from models.account import Account
from models.model import App, UploadFile


class Dataset(db.Model):
    __tablename__ = "datasets"
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='dataset_pkey'),
        db.Index('dataset_tenant_idx', 'tenant_id'),
    )
    INDEXING_TECHNIQUE_LIST = ['high_quality', 'economy']

    id = db.Column(UUID, server_default=db.text("uuid_generate_v4()"))
    tenant_id = db.Column(UUID, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    provider = db.Column(db.String(255), nullable=False,
                         server_default=db.text("'vendor'::character varying"))
    permission = db.Column(db.String(255), nullable=False,
                           server_default=db.text("'only_me'::character varying"))
    data_source_type = db.Column(db.String(255))
    indexing_technique = db.Column(db.String(255), nullable=True)
    index_struct = db.Column(db.Text, nullable=True)
    created_by = db.Column(UUID, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    updated_by = db.Column(UUID, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))


class DatasetProcessRule(db.Model):
    __tablename__ = 'dataset_process_rules'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='dataset_process_rule_pkey'),
        db.Index('dataset_process_rule_dataset_id_idx', 'dataset_id'),
    )

    id = db.Column(UUID, nullable=False,
                   server_default=db.text('uuid_generate_v4()'))
    dataset_id = db.Column(UUID, nullable=False)
    mode = db.Column(db.String(255), nullable=False,
                     server_default=db.text("'automatic'::character varying"))
    rules = db.Column(db.Text, nullable=True)
    created_by = db.Column(UUID, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))

    MODES = ["automatic", "custom"]
    PRE_PROCESSING_RULES = ['remove_stopwords',
                            'remove_extra_spaces', 'remove_urls_emails']
    AUTOMATIC_RULES = {
        'pre_processing_rules': [
            {'id': 'remove_extra_spaces', 'enabled': True},
            {'id': 'remove_urls_emails', 'enabled': False}
        ],
        'segmentation': {
            'delimiter': '\n',
            'max_tokens': 1000
        }
    }

    def to_dict(self):
        return {
            'id': self.id,
            'dataset_id': self.dataset_id,
            'mode': self.mode,
            'rules': self.rules_dict,
            'created_by': self.created_by,
            'created_at': self.created_at,
        }

    @property
    def rules_dict(self):
        try:
            return json.loads(self.rules) if self.rules else None
        except JSONDecodeError:
            return None


class Document(db.Model):
    __tablename__ = 'documents'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='document_pkey'),
        db.Index('document_dataset_id_idx', 'dataset_id'),
        db.Index('document_is_paused_idx', 'is_paused'),
    )
    id = db.Column(UUID, nullable=False,
                   server_default=db.text('uuid_generate_v4()'))
    tenant_id = db.Column(UUID, nullable=False)
    dataset_id = db.Column(UUID, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    data_source_type = db.Column(db.String(255), nullable=False)
    data_source_info = db.Column(db.Text, nullable=True)
    dataset_process_rule_id = db.Column(UUID, nullable=True)
    batch = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_from = db.Column(db.String(255), nullable=False)
    created_by = db.Column(UUID, nullable=False)
    created_api_request_id = db.Column(UUID, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    # start processing
    processing_started_at = db.Column(db.DateTime, nullable=True)

    # parsing
    file_id = db.Column(db.Text, nullable=True)
    word_count = db.Column(db.Integer, nullable=True)
    parsing_completed_at = db.Column(db.DateTime, nullable=True)

    # cleaning
    cleaning_completed_at = db.Column(db.DateTime, nullable=True)

    # split
    splitting_completed_at = db.Column(db.DateTime, nullable=True)

    # indexing
    tokens = db.Column(db.Integer, nullable=True)
    indexing_latency = db.Column(db.Float, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    # pause
    is_paused = db.Column(db.Boolean, nullable=True,
                          server_default=db.text('false'))
    paused_by = db.Column(UUID, nullable=True)
    paused_at = db.Column(db.DateTime, nullable=True)

    # error
    error = db.Column(db.Text, nullable=True)
    stopped_at = db.Column(db.DateTime, nullable=True)
    
    # basic fields
    indexing_status = db.Column(db.String(
        255), nullable=False, server_default=db.text("'waiting'::character varying"))
    enabled = db.Column(db.Boolean, nullable=False,
                        server_default=db.text('true'))
    disabled_at = db.Column(db.DateTime, nullable=True)
    disabled_by = db.Column(UUID, nullable=True)
    archived = db.Column(db.Boolean, nullable=False,
                         server_default=db.text('false'))
    archived_reason = db.Column(db.String(255), nullable=True)
    archived_by = db.Column(UUID, nullable=True)
    archived_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    doc_type = db.Column(db.String(40), nullable=True)
    doc_metadata = db.Column(db.JSON, nullable=True)

    DATA_SOURCES = ['upload_file']

