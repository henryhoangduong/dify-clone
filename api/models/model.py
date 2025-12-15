import json

from flask import current_app
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from libs.helper import generate_string
from extensions.ext_database import db
from .account import Account, Tenant


class DifySetup(db.Model):
    __tablename__ = 'dify_setups'
    __table_args__ = (
        db.PrimaryKeyConstraint('version', name='dify_setup_pkey'),
    )
    version = db.Column(db.String(255), nullable=False)
    setup_at = db.Column(db.DateTime, nullable=False,
                         server_default=db.text('CURRENT_TIMESTAMP(0)'))


class App(db.Model):
    __tablename__ = 'apps'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='app_pkey'),
        db.Index('app_tenant_id_idx', 'tenant_id')
    )

    id = db.Column(UUID, server_default=db.text('uuid_generate_v4()'))
    tenant_id = db.Column(UUID, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    mode = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(255))
    icon_background = db.Column(db.String(255))
    app_model_config_id = db.Column(UUID, nullable=True)
    status = db.Column(db.String(255), nullable=False,
                       server_default=db.text("'normal'::character varying"))
    enable_site = db.Column(db.Boolean, nullable=False)
    enable_api = db.Column(db.Boolean, nullable=False)
    api_rpm = db.Column(db.Integer, nullable=False)
    api_rph = db.Column(db.Integer, nullable=False)
    is_demo = db.Column(db.Boolean, nullable=False,
                        server_default=db.text('false'))
    is_public = db.Column(db.Boolean, nullable=False,
                          server_default=db.text('false'))
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))

    @property
    def site(self):
        site = db.session.query(Site).filter(Site.app_id == self.id).first()
        return site

    @property
    def app_model_config(self):
        app_model_config = db.session.query(AppModelConfig).filter(
            AppModelConfig.id == self.app_model_config_id).first()
        return app_model_config

    @property
    def api_base_url(self):
        return current_app.config['API_URL'] + '/v1'

    @property
    def tenant(self):
        tenant = db.session.query(Tenant).filter(
            Tenant.id == self.tenant_id).first()
        return tenant


class AppModelConfig(db.Model):
    __tablename__ = 'app_model_configs'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='app_model_config_pkey'),
        db.Index('app_app_id_idx', 'app_id')
    )

    id = db.Column(UUID, server_default=db.text('uuid_generate_v4()'))
    app_id = db.Column(UUID, nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    model_id = db.Column(db.String(255), nullable=False)
    configs = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    opening_statement = db.Column(db.Text)
    suggested_questions = db.Column(db.Text)
    suggested_questions_after_answer = db.Column(db.Text)
    more_like_this = db.Column(db.Text)
    model = db.Column(db.Text)
    user_input_form = db.Column(db.Text)
    pre_prompt = db.Column(db.Text)
    agent_mode = db.Column(db.Text)

    @property
    def app(self):
        app = db.session.query(App).filter(App.id == self.app_id).first()
        return app

    @property
    def model_dict(self) -> dict:
        return json.loads(self.model) if self.model else None

    @property
    def suggested_questions_list(self) -> list:
        return json.loads(self.suggested_questions) if self.suggested_questions else []

    @property
    def suggested_questions_after_answer_dict(self) -> dict:
        return json.loads(self.suggested_questions_after_answer) if self.suggested_questions_after_answer \
            else {"enabled": False}

    @property
    def more_like_this_dict(self) -> dict:
        return json.loads(self.more_like_this) if self.more_like_this else {"enabled": False}

    @property
    def user_input_form_list(self) -> dict:
        return json.loads(self.user_input_form) if self.user_input_form else []

    @property
    def agent_mode_dict(self) -> dict:
        return json.loads(self.agent_mode) if self.agent_mode else {"enabled": False, "tools": []}


class RecommendedApp(db.Model):
    __tablename__ = 'recommended_apps'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='recommended_app_pkey'),
        db.Index('recommended_app_app_id_idx', 'app_id'),
        db.Index('recommended_app_is_listed_idx', 'is_listed')
    )

    id = db.Column(UUID, primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))
    app_id = db.Column(UUID, nullable=False)
    description = db.Column(db.JSON, nullable=False)
    copyright = db.Column(db.String(255), nullable=False)
    privacy_policy = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    is_listed = db.Column(db.Boolean, nullable=False, default=True)
    install_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))

    @property
    def app(self):
        app = db.session.query(App).filter(App.id == self.app_id).first()
        return app

    # def set_description(self, lang, desc):
    #     if self.description is None:
    #         self.description = {}
    #     self.description[lang] = desc

    def get_description(self, lang):
        if self.description and lang in self.description:
            return self.description[lang]
        else:
            return self.description.get('en')


class InstalledApp(db.Model):
    __tablename__ = 'installed_apps'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='installed_app_pkey'),
        db.Index('installed_app_tenant_id_idx', 'tenant_id'),
        db.Index('installed_app_app_id_idx', 'app_id'),
        db.UniqueConstraint('tenant_id', 'app_id', name='unique_tenant_app')
    )

    id = db.Column(UUID, server_default=db.text('uuid_generate_v4()'))
    tenant_id = db.Column(UUID, nullable=False)
    app_id = db.Column(UUID, nullable=False)
    app_owner_tenant_id = db.Column(UUID, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    is_pinned = db.Column(db.Boolean, nullable=False,
                          server_default=db.text('false'))
    last_used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP(0)'))

    @property
    def app(self):
        app = db.session.query(App).filter(App.id == self.app_id).first()
        return app

    @property
    def tenant(self):
        tenant = db.session.query(Tenant).filter(
            Tenant.id == self.tenant_id).first()
        return tenant

