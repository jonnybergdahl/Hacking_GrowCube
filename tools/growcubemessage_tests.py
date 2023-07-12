import unittest
from growcube_client.growcubemessage import GrowcubeMessage


class GrowcubeMessageTests(unittest.TestCase):

    def test_empty(self):
        data = b''
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(0, new_index)
        self.assertIsNone(command)
        self.assertIsNone(payload)

    def test_incomplete_header(self):
        data = b'ele'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(0, new_index)
        self.assertIsNone(command)
        self.assertIsNone(payload)

    def test_incomplete_header_with_command(self):
        data = b'elea01'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(0, new_index)
        self.assertIsNone(command)
        self.assertIsNone(payload)

    def test_incomplete_header_with_command_and_length(self):
        data = b'elea01#1#'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(0, new_index)
        self.assertIsNone(command)
        self.assertIsNone(payload)

    def test_incomplete_header_with_command_and_length_and_data(self):
        data = b'elea01#1#x'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(0, new_index)
        self.assertIsNone(command)
        self.assertIsNone(payload)

    def test_complete_message(self):
        data = b'elea28#1#0#'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(11, new_index)
        self.assertIsNone(command)
        self.assertEqual("0", payload)

    def test_complete_message_with_crap_at_end(self):
        data = b'elea24#12#3.6@12663500#abcdef'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(23, new_index)
        self.assertIsNone(command)
        self.assertEqual("3.6@12663500", payload)
        self.assertEqual(data[new_index:], b"abcdef")

    def test_complete_with_crap_at_start(self):
        data = b'crapelea24#12#3.6@12663500#'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(27, new_index)
        self.assertIsNone(command)
        self.assertEqual("3.6@12663500", payload)
        self.assertEqual(data[new_index:], b"")

    def test_incomplete_with_crap_at_start(self):
        data = b'crapelea24#12#3.6@12663500'
        new_index, command, payload = GrowcubeMessage.from_bytes(data)
        self.assertEqual(4, new_index)
        self.assertIsNone(command)
        self.assertIsNone(payload)
        self.assertEqual(data[new_index:], b"elea24#12#3.6@12663500")


if __name__ == '__main__':
    unittest.main()