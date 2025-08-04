from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from projects.models import Project, ProjectMember, ProjectStage, ProjectContextEngine
from files.models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
User = get_user_model()

class ProjectAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="taha", password="test123")
        self.stage = ProjectStage.objects.create(name="Ideation", order=1)
        self.client.login(username="taha", password="test123")

    @patch('projects.analysis.dpg_summary_tool.func') # Mock the summary tool as well if it makes API calls
    @patch('projects.signals.trigger_ai_analysis')
    def test_create_project(self, mock_trigger_analysis, mock_summary_tool):
        url = "/api/projects/"
        data = {
            "name": "Test Project",
            "description": "A sample project",
            "status": Project.ProjectStatus.ACTIVE,
            "stage": self.stage.name,
            "category": "Electronics"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().owner, self.user)

        project = Project.objects.first()
        self.assertTrue(ProjectMember.objects.filter(user=self.user, project=project).exists())
        self.assertEqual(ProjectMember.objects.get(user=self.user, project=project).role, ProjectMember.MemberRole.OWNER)

    def test_list_projects(self):
        project = Project.objects.create(
            name="Proj1",
            owner=self.user,
            stage=self.stage
        )
        ProjectMember.objects.create(user=self.user, project=project, role=ProjectMember.MemberRole.OWNER)
        url = "/api/projects/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_role_assignment(self):
        project = Project.objects.create(name="Proj2", owner=self.user, stage=self.stage)
        ProjectMember.objects.create(user=self.user, project=project, role=ProjectMember.MemberRole.OWNER)
        member = User.objects.create_user(username="member", password="pass123")
        ProjectMember.objects.create(user=member, project=project, role=ProjectMember.MemberRole.VIEWER)
        self.assertEqual(project.memberships.get(user=member).role, ProjectMember.MemberRole.VIEWER)

    
    # Use @patch to prevent the real function from being called
    @patch('projects.signals.trigger_ai_analysis')
    def test_upload_file_and_trigger_context_engine(self, mock_trigger_analysis):
        project = Project.objects.create(name="AI Project", owner=self.user, stage=self.stage)
        ProjectMember.objects.create(user=self.user, project=project, role=ProjectMember.MemberRole.OWNER)
        url = f"/api/projects/{project.pk}/files/"
        file = SimpleUploadedFile("test.txt", b"This is a design file for the project.")

        response = self.client.post(url, {"file": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UploadedFile.objects.filter(project=project).exists())
        # Assert that your analysis function was called once
        mock_trigger_analysis.assert_called_once()

class ProjectMemberTest(APITestCase):

    def setUp(self):
        self.patcher = patch('projects.signals.trigger_ai_analysis')
        self.mock_trigger_analysis = self.patcher.start()
        self.owner = User.objects.create_user(username="owner", password="test123")
        self.project = Project.objects.create(name="Owner Project", owner=self.owner)
        ProjectMember.objects.create(user=self.owner, project=self.project, role=ProjectMember.MemberRole.OWNER)
        self.client.login(username="owner", password="test123")

        self.member_user = User.objects.create_user(username="member", password="pass123")
    
    def tearDown(self):
        # Stop the patcher after each test to ensure clean state
        self.patcher.stop()

    def test_add_member(self):
        url = f"/api/projects/{self.project.pk}/add_member/"
        data = {"user": self.member_user.id, "role": ProjectMember.MemberRole.EDITOR}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProjectMember.objects.filter(user=self.member_user, project=self.project).exists())

    def test_only_owner_can_add_member(self):
        self.client.logout()
        self.client.login(username="member", password="pass123")
        url = f"/api/projects/{self.project.pk}/add_member/"
        data = {"user": self.member_user.id, "role": ProjectMember.MemberRole.EDITOR}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_update_role(self):
        ProjectMember.objects.create(user=self.member_user, project=self.project, role=ProjectMember.MemberRole.VIEWER)
        url = f"/api/projects/{self.project.pk}/update_member/"
        data = {"user": self.member_user.id, "role": ProjectMember.MemberRole.EDITOR}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(ProjectMember.objects.get(user=self.member_user, project=self.project).role, ProjectMember.MemberRole.EDITOR)

    def test_remove_member(self):
        ProjectMember.objects.create(user=self.member_user, project=self.project, role=ProjectMember.MemberRole.VIEWER)
        url = f"/api/projects/{self.project.pk}/remove_member/"
        response = self.client.delete(url, {"user": self.member_user.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ProjectMember.objects.filter(user=self.member_user, project=self.project).exists())
