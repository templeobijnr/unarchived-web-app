from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from projects.models import Project, ProjectMember, ProjectStage
from rest_framework.authtoken.models import Token

class ProjectAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="taha", password="test123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_project(self):
        stage = ProjectStage.objects.create(name="Ideation", order=1)
        response = self.client.post("/api/projects/", {
            "name": "Unarchived Core",
            "description": "DPG + RFQ System",
            "stage": stage.name,
            "status": "ACTIVE"
        }, format='json')
        print("Create response:", response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 1)

    def test_list_projects(self):
        project = Project.objects.create(name="Proj A", description="Test", owner=self.user)
        ProjectMember.objects.create(user=self.user, project=project, role=ProjectMember.MemberRole.OWNER)
        response = self.client.get("/api/projects/")
        print("List response:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_role_assignment(self):
        Project.objects.all().delete()
        project = Project.objects.create(name="Test Project", description="123", owner=self.user)
        ProjectMember.objects.create(user=self.user, project=project, role=ProjectMember.MemberRole.OWNER)
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
        projects = response.data
        if isinstance(projects, dict) and 'results' in projects:
            projects = projects['results']  

        self.assertGreater(len(projects), 0)
        print("Role response:", response.data)
        project_data = response.data['results'][0]  
        self.assertEqual(project_data['role'], 'OWNER')

class ProjectMemberTest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="test123")
        self.editor = User.objects.create_user(username="editor", password="test123")
        self.viewer = User.objects.create_user(username="viewer", password="test123")
        self.project = Project.objects.create(name="Collab Project", description="With Members", owner=self.owner)
        ProjectMember.objects.create(user=self.owner, project=self.project, role=ProjectMember.MemberRole.OWNER)

        self.token = Token.objects.create(user=self.owner)
        self.not_owner = Token.objects.create(user=self.viewer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_add_member(self):
        res = self.client.post(f"/api/projects/{self.project.id}/add_member/", {
            "user": self.editor.id,
            "role": ProjectMember.MemberRole.EDITOR
        }, format='json')
        print("Add Member Response:", res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(ProjectMember.objects.count(), 2)

    def test_update_member_role(self):
        ProjectMember.objects.create(user=self.editor, project=self.project, role=ProjectMember.MemberRole.VIEWER)
        res = self.client.patch(f"/api/projects/{self.project.id}/update_member/", {
            "user": self.editor.id,
            "role": ProjectMember.MemberRole.EDITOR
        }, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(ProjectMember.objects.get(user=self.editor).role, ProjectMember.MemberRole.EDITOR)

    def test_remove_member(self):
        ProjectMember.objects.create(user=self.viewer, project=self.project, role=ProjectMember.MemberRole.VIEWER)
        res = self.client.delete(f"/api/projects/{self.project.id}/remove_member/", {
            "user": self.viewer.id
        }, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(ProjectMember.objects.filter(user=self.viewer).count(), 0)

    def test_only_owner_can_add_member(self):
        intruder = User.objects.create_user(username="intruder", password="nopass")
        intruder_token = Token.objects.create(user=intruder)
    
        # Owner creates a new project and adds themselves
        project = Project.objects.create(name="Restricted Project", description="Owner Only", owner=self.owner)
        ProjectMember.objects.create(user=self.owner, project=project, role=ProjectMember.MemberRole.OWNER)
    
        # Now act as intruder (not part of the project)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + intruder_token.key)
    
        # Try to add a member
        res = self.client.post(f"/api/projects/{project.id}/add_member/", {
            "user": self.editor.id,
            "role": "viewer"
        }, format='json')
        print("Status:", res.status_code)
        print("Data:", res.data)

        self.assertEqual(res.status_code, 403)
    
    def test_only_owner_can_update_role(self):
        # Creating editor, adding to project
        ProjectMember.objects.create(user=self.editor, project=self.project, role=ProjectMember.MemberRole.EDITOR)

        # Logging in as editor
        editor_token = Token.objects.create(user=self.editor)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + editor_token.key)

        # Try to update their role
        res = self.client.patch(f"/api/projects/{self.project.id}/update_member/", {
            "user": self.editor.id,
            "role": ProjectMember.MemberRole.OWNER
        }, format='json')

        self.assertEqual(res.status_code, 403)
        self.assertEqual(ProjectMember.objects.get(user=self.editor).role, ProjectMember.MemberRole.EDITOR)