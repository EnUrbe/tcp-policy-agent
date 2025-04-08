
---

## 🧪 `test/test_endpoints.py`

```python
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def test_state_bills(self):
        tester = app.test_client(self)
        response = tester.get('/api/state_bills?state=Colorado&keyword=mental+health')
        self.assertEqual(response.status_code, 200)

    def test_federal_bills(self):
        tester = app.test_client(self)
        response = tester.get('/api/federal_bills?keyword=health+equity')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

