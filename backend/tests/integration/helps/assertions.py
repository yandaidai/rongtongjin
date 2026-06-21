def assert_response_success(response, expected_data):
    """断言响应状态码"""
    assert response.status_code == 200, f"预期状态码 200，实际 {response.status_code}"
    data = response.json()
    assert data["code"] == 0, f"预期 code 0，实际 {data['code']}"
    assert data["data"] == expected_data, f"预期 data {expected_data}，实际 {data['data']}"


def assert_response_error(response, expected_code, expected_message):
    """断言响应错误"""
    assert response.status_code == 200, f"预期状态码 200，实际 {response.status_code}"
    data = response.json()
    assert data["code"] == expected_code, f"预期 code {expected_code}，实际 {data['code']}"
    assert expected_message in data["message"], f"预期 message 包含 '{expected_message}'，实际 '{data['message']}'"