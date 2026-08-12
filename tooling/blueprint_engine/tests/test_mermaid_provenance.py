from blueprint_engine.mermaid_provenance import git_blob_sha

def test_git_blob_sha_matches_git_object_format():
    # Well-known Git blob construction: sha1("blob <len>\\0" + content)
    assert git_blob_sha(b"test\n") == "9daeafb9864cf43055ae93beb0afd6c7d144bfa4"
