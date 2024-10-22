import asyncio

from aiokeycloak.factory import KeycloakClientFactory
from aiokeycloak.sessions.aiohttp import AioHTTPKeycloakSession
from aiokeycloak.types.user import User


ACCESS_TOKEN = \
    'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuQkJsMnFzWERGOEYxMVJlcHBsUXZjY3lyeXV1Y2pDMHluZXJlNlBwMTZrIn0.eyJleHAiOjE3Mjk2NjE5MzEsImlhdCI6MTcyOTYyNTkzNiwiYXV0aF90aW1lIjoxNzI5NjI1OTMxLCJqdGkiOiIyNzkxNDRiZC1iZmVhLTRmNmEtODA0Ni04YzQyYzQwZWRmZDMiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODEvcmVhbG1zL2pvcGEiLCJhdWQiOlsicmVhbG0tbWFuYWdlbWVudCIsImJyb2tlciIsImFjY291bnQiXSwic3ViIjoiYWNiZWI5ZGQtNzYzMS00MDIxLTg4YjgtOTBiZjIzMmE4NDA5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiY2xpZW50X2lkIiwic2lkIjoiODk3ZGI5M2ItNDgxZi00MmMwLWFmYTAtM2IyMzIxZTUwNWQ3IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL29hdXRoLnBzdG1uLmlvIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLWpvcGEiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsicmVhbG0tbWFuYWdlbWVudCI6eyJyb2xlcyI6WyJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsInZpZXctcmVhbG0iLCJtYW5hZ2UtaWRlbnRpdHktcHJvdmlkZXJzIiwiaW1wZXJzb25hdGlvbiIsInJlYWxtLWFkbWluIiwiY3JlYXRlLWNsaWVudCIsIm1hbmFnZS11c2VycyIsInF1ZXJ5LXJlYWxtcyIsInZpZXctYXV0aG9yaXphdGlvbiIsInF1ZXJ5LWNsaWVudHMiLCJxdWVyeS11c2VycyIsIm1hbmFnZS1ldmVudHMiLCJtYW5hZ2UtcmVhbG0iLCJ2aWV3LWV2ZW50cyIsInZpZXctdXNlcnMiLCJ2aWV3LWNsaWVudHMiLCJtYW5hZ2UtYXV0aG9yaXphdGlvbiIsIm1hbmFnZS1jbGllbnRzIiwicXVlcnktZ3JvdXBzIl19LCJicm9rZXIiOnsicm9sZXMiOlsicmVhZC10b2tlbiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsInZpZXctYXBwbGljYXRpb25zIiwidmlldy1jb25zZW50Iiwidmlldy1ncm91cHMiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsImRlbGV0ZS1hY2NvdW50IiwibWFuYWdlLWNvbnNlbnQiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6ImEgQkJCIiwicHJlZmVycmVkX3VzZXJuYW1lIjoid2VydCIsImdpdmVuX25hbWUiOiJhIiwiZmFtaWx5X25hbWUiOiJCQkIiLCJlbWFpbCI6Im1tc3N2dnZ2NTcwQGdtYWlsLmNvbSJ9.S1itDMcvVkoHFn0IPQV61Wnzuhn4UVb4Fz2BRSJMFlymjl3NFdP0My97X-VrIf2DagXiInsf8JcNg4tegNBt5cKzq_xgrCEX2ILCE-Vu8SzP6iRo54PV7JQD2RFSLhM3ascxCs9csXF5Mi2TITxcx3FA7EEnKY2p-K6GWd-cWiYZmSMKFCVgN3mRd3MAJ5AUdCJslJBAV28K1V4_aMCUVGFhZ5ltx_NQbTUoMorwpzK6FYgjVzzsT9owGFoFHc_4bpGWkVgYMILp8C8WtZkN0MvyIKgT10br_gu1daq_qJWBoEorU-5VU8cKDky2kKgOSW2y_qEHvb1WQ6HwAXz7XA'
REALM_NAME = 'jopa'


async def main() -> None:
    client_factory = KeycloakClientFactory(
        AioHTTPKeycloakSession('http://localhost:8081'),
    )
    async with client_factory:
        client = client_factory.factory(ACCESS_TOKEN)
        a = await client.create_user(
            realm_name=REALM_NAME,
            user=User(
                first_name='A',
                username='BBdaaaedddaBBDD',
                email_verified=True,
                email='aaaaedeaaa@gmail.com',
                enabled=True,
            ),
        )
        print(a)


asyncio.run(main())
