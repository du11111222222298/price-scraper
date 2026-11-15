import pytest


@pytest.mark.parametrize(
    "product_id, expected_status",
    [
        (1, 200),
        (2, 200),
        (9999, 404),
    ],
)
def test_get_post_or_product(api_client, product_id, expected_status):
  response = api_client.get(f"/posts/{product_id}")
  assert (
      response.status_code == expected_status
  ), f"Expected {expected_status}, got {response.status_code}"

  if expected_status == 200:
    data = response.json()
    assert "id" in data
    assert "title" in data