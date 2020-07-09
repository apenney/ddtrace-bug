from __future__ import unicode_literals

from failure.core.enumerations import Enumeration
from rolepermissions.roles import AbstractUserRole
from six import iteritems

"""
/!\ Attention /!\

ANY MODIFICATION TO THIS FILE IS SUBJECT TO REVIEW AND APPROVAL FROM
A SENIOR ENGINEER. YOU CANNOT APPROVE YOURSELF.
"""

class PermissionNames(Enumeration):
    """
    Enumeration of all the available permissions. If we decide to add new
    permissions, we must make sure we add it to this class
    """
    # Flows
    FLOWS_VIEW = 'flows_view'
    FLOWS_EDIT = 'flows_edit'
    FLOWS_LAUNCH = 'flows_launch'
    FLOWS_DELETE = 'flows_delete'

    # Segmentation
    SEGMENTS_VIEW_DEFINITIONS = 'segments_view_definitions'
    SEGMENTS_EDIT = 'segments_edit'
    SEGMENTS_EDIT_LIVE = 'segments_edit_live'
    SEGMENTS_DELETE = 'segments_delete'
    SEGMENTS_VIEW_STATS = 'segments_view_stats'

    # Results /
    RESULTS_VIEW_FLOW_RESULTS = 'results_view_flow_results'
    RESULTS_VIEW_FLOW_REPORTING = 'results_view_flow_reporting'
    RESULTS_EDIT = 'results_edit'
    RESULTS_DELETE = 'results_delete'

    # Data import, export, & destruction
    DATA_EXPORT_SEGMENTS = 'data_export_segments'
    DATA_EXPORT_FLOW_MEMBERSHIPS = 'data_export_flow_memberships'
    DATA_EXPORT_RESULTS = 'data_export_results'
    DATA_CONFIGURE_FEEDS = 'data_configure_feeds'
    # TODO(kevin): Not sure if this needs to be rolled down into SQL, or if we
    # just delete it
    # DATA_CREATE_SETS = 'data_create_sets'
    DATA_SUBMIT_PRIVACY_REQUESTS = 'data_submit_privacy_requests'

    # SQL development
    SQL_VIEW_DATASETS = 'sql_view_datasets'
    SQL_SAMPLE_DATASETS = 'sql_sample_datasets'
    # TODO(kevin): delete this permission. Same as EDIT
    SQL_CONFIGURE_DATASETS = 'sql_configure_datasets'
    SQL_EDIT_DATASETS = 'sql_edit_datasets'
    SQL_DRILLDOWN = 'sql_drilldown'

    # Content management
    CONTENT_VIEW = 'content_view'
    CONTENT_EDIT = 'content_edit'
    CONTENT_DELETE = 'content_delete'

    # Other
    OTHER_VIEW_DOCUMENTATION = 'other_view_documentation'
    ADMINISTRATE_USERS = 'administrate_users'

    # Integrations
    INTEGRATIONS_VIEW = 'integrations_view'
    INTEGRATIONS_EDIT = 'integrations_edit'

    # Organization Settings
    ORG_SETTINGS_VIEW = 'org_settings_view'
    ORG_SETTINGS_EDIT = 'org_settings_edit'

    # Contacts (Single Contact/Voyager)
    CONTACTS_VIEW = 'contacts_view'


def merge(*roles):
    """Merge the permissions of one or more Roles"""
    perms = [r if isinstance(r, dict) else r.available_permissions
             for r in roles]
    return dict(item for d in perms for item in iteritems(d))


"""
ROLES (combination of permissions)
"""


class FlowsViewer(AbstractUserRole):
    """A role that is allowed to view flows"""
    available_permissions = merge(
        {
            PermissionNames.FLOWS_VIEW: True,
        })


class FlowsUser(AbstractUserRole):
    """A role that is allowed to modify flows. Also a FlowsViewer"""
    available_permissions = merge(
        FlowsViewer,
        {
            PermissionNames.FLOWS_EDIT: True,
            PermissionNames.FLOWS_LAUNCH: True,
            PermissionNames.FLOWS_DELETE: True,
        })


class SegmentationViewer(AbstractUserRole):
    """A role that is allowed to view segments"""
    available_permissions = merge(
        {
            PermissionNames.SEGMENTS_VIEW_STATS: True,
        })


class SegmentationUser(AbstractUserRole):
    """
    A role that is allowed to modify segments and view segment definitions.
    Also a SegmentationViewer
    """
    available_permissions = merge(
        SegmentationViewer,
        {
            PermissionNames.SEGMENTS_VIEW_DEFINITIONS: True,
            PermissionNames.SEGMENTS_EDIT: True,
            PermissionNames.SEGMENTS_EDIT_LIVE: True,
            PermissionNames.SEGMENTS_DELETE: True,
        })


class ResultsViewer(AbstractUserRole):
    """
    A role that is allowed to view results/reporting
    """
    available_permissions = merge(
        {
            PermissionNames.RESULTS_VIEW_FLOW_RESULTS: True,
            PermissionNames.RESULTS_VIEW_FLOW_REPORTING: True,
        })


class ResultsUser(AbstractUserRole):
    """
    A role that is allowed to create results/reporting
    """
    available_permissions = merge(
        ResultsViewer,
        {
            PermissionNames.RESULTS_EDIT: True,
            PermissionNames.RESULTS_DELETE: True,
        })


class DataUser(AbstractUserRole):
    """A role that is allowed to export and modify data segments"""
    available_permissions = merge(
        {
            PermissionNames.DATA_EXPORT_SEGMENTS: True,
            PermissionNames.DATA_EXPORT_FLOW_MEMBERSHIPS: True,
            PermissionNames.DATA_EXPORT_RESULTS: True,
            PermissionNames.DATA_CONFIGURE_FEEDS: True,
            PermissionNames.DATA_SUBMIT_PRIVACY_REQUESTS: True,
        })


class SqlViewer(AbstractUserRole):
    """A role that is allowed to view datasets generated from S3QL"""
    available_permissions = merge(
        {
            PermissionNames.SQL_VIEW_DATASETS: True,
        })


class SqlUser(AbstractUserRole):
    """A role that is allowed to drilldown deeper into S3QL datasets"""
    available_permissions = merge(
        SqlViewer,
        {
            PermissionNames.SQL_SAMPLE_DATASETS: True,
            PermissionNames.SQL_DRILLDOWN: True,
        })


class SqlDeveloper(AbstractUserRole):
    """A role that is allowed to modify S3QL datasets"""
    available_permissions = merge(
        SqlUser,
        {
            PermissionNames.SQL_CONFIGURE_DATASETS: True,
            PermissionNames.SQL_EDIT_DATASETS: True,
        })


class ContentViewer(AbstractUserRole):
    """
    A role that is allowed to view the contents list page (templates, content
    blocks, images, etc), view individual pieces of content, and use them in
    the flow builder.
    """
    available_permissions = merge(
        {
            PermissionNames.CONTENT_VIEW: True,
        })


class ContentUser(AbstractUserRole):
    """
    A role that is allowed to create and edit pieces of content via the content
    editor interface
    """
    available_permissions = merge(
        ContentViewer,
        {
            PermissionNames.CONTENT_EDIT: True,
            PermissionNames.CONTENT_DELETE: True,
        })


class DocumentationViewer(AbstractUserRole):
    """A role that is allowed to view documentation"""
    available_permissions = merge(
        {
            PermissionNames.OTHER_VIEW_DOCUMENTATION: True,
        })


class UsersManagement(AbstractUserRole):
    """A role that is able to modify users' roles"""
    available_permissions = merge(
        {
            PermissionNames.ADMINISTRATE_USERS: True,
        })


class IntegrationsViewer(AbstractUserRole):
    """A role that is able to view integration credentials"""
    available_permissions = merge(
        {
            PermissionNames.INTEGRATIONS_VIEW: True,
        })


class IntegrationsUser(AbstractUserRole):
    """A role that is able to modify integration credentials"""
    available_permissions = merge(
        IntegrationsViewer,
        {
            PermissionNames.INTEGRATIONS_EDIT: True,
        }
    )


class OrganizationSettingsViewer(AbstractUserRole):
    """A role that is able to view organization settings"""
    available_permissions = merge(
        {
            PermissionNames.ORG_SETTINGS_VIEW: True,
        }
    )


class OrganizationSettingsUser(AbstractUserRole):
    """A role that is able to modify integration credentials"""
    available_permissions = merge(
        OrganizationSettingsViewer,
        {
            PermissionNames.ORG_SETTINGS_EDIT: True,
        }
    )


class ContactsViewer(AbstractUserRole):
    """A role that is able to view pages related to single contact view"""
    available_permissions = merge(
        {
            PermissionNames.CONTACTS_VIEW: True,
        })


class OrgAdmin(AbstractUserRole):
    """A super-role that can do everything in an Organization"""
    available_permissions = merge(
        FlowsUser,
        SegmentationUser,
        ResultsUser,
        DataUser,
        SqlDeveloper,
        ContentUser,
        DocumentationViewer,
        UsersManagement,
        IntegrationsUser,
        ContactsViewer,
        OrganizationSettingsUser,
    )


class OrgUser(AbstractUserRole):
    """
    A super-role that can do much in an Organization.
    Limited to SqlUser permissions
    """
    available_permissions = merge(
        FlowsUser,
        SegmentationUser,
        ResultsUser,
        DataUser,
        SqlDeveloper,
        ContentUser,
        DocumentationViewer,
        IntegrationsUser,
        ContactsViewer,
        OrganizationSettingsViewer,
    )


class OrgViewer(AbstractUserRole):
    """A super-role that has a read-only view of an Organization"""
    available_permissions = merge(
        FlowsViewer,
        SegmentationViewer,
        ResultsViewer,
        SqlViewer,
        ContentViewer,
        IntegrationsViewer,
        OrganizationSettingsViewer,
        ContactsViewer,
    )


class Custom(AbstractUserRole):
    """
    A super-role that can do everything in an Organization if granted the
    permissions individually, but cannot do anything by default.
    """
    available_permissions = dict((k, False) for k in list(PermissionNames.values()))


FRONTEND_ROLES = [Custom, OrgAdmin, OrgUser, OrgViewer]
ORG_ROLES = [OrgAdmin, OrgUser, OrgViewer]
