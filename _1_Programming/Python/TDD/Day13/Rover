import unittest
from Rover import Rover, MeetObstacleException
from Command import Command
from Field import Field


class testCases(unittest.TestCase):
    def testRover(self):
        rover = Rover((3, 5), 'N')
        self.assertEqual(3, rover.x)
        self.assertEqual(5, rover.y)
        self.assertEqual('N', rover.orientation)

    def testMoveFoward(self):
        rover = Rover((3, 5), 'N')
        field = Field(100, 100)
        rover.moveFoward(field)
        self.assertEqual(3, rover.x)
        self.assertEqual(6, rover.y)
        self.assertEqual('N', rover.orientation)
        rover = Rover((3, 5), 'S')
        rover.moveFoward(field)
        self.assertEqual(3, rover.x)
        self.assertEqual(4, rover.y)
        rover = Rover((3, 5), 'E')
        rover.moveFoward(field)
        self.assertEqual(4, rover.x)
        self.assertEqual(5, rover.y)
        rover = Rover((3, 5), 'W')
        rover.moveFoward(field)
        self.assertEqual(2, rover.x)
        self.assertEqual(5, rover.y)

    def testMoveBack(self):
        rover = Rover((3, 5), 'N')
        field = Field(100, 100)
        rover.moveBack(field)
        self.assertEqual(3, rover.x)
        self.assertEqual(4, rover.y)
        rover = Rover((3, 5), 'W')
        rover.moveBack(field)
        self.assertEqual(4, rover.x)
        self.assertEqual(5, rover.y)

    def testTurnLeft(self):
        rover = Rover((3, 5), 'N')
        field = Field(100, 100)
        rover.turnLeft(field)
        self.assertEqual(3, rover.x)
        self.assertEqual(5, rover.y)
        self.assertEqual('W', rover.orientation)
        rover.turnLeft(field)
        self.assertEqual('S', rover.orientation)
        rover.turnLeft(field)
        self.assertEqual('E', rover.orientation)
        rover.turnLeft(field)
        self.assertEqual('N', rover.orientation)

    def testTurnRight(self):
        field = Field(100, 100)
        rover = Rover((3, 5), 'N')
        rover.turnRight(field)
        self.assertEqual(3, rover.x)
        self.assertEqual(5, rover.y)
        self.assertEqual('E', rover.orientation)
        rover.turnRight(field)
        self.assertEqual('S', rover.orientation)
        rover.turnRight(field)
        self.assertEqual('W', rover.orientation)
        rover.turnRight(field)
        self.assertEqual('N', rover.orientation)

    def testCommand(self):
        cmd = 'I 10 10;V 3 5 N'
        command = Command(cmd)
        self.assertEqual(command.field.X, 10)
        self.assertEqual(command.field.Y, 10)
        self.assertEqual(command.rover.x, 3)
        self.assertEqual(command.rover.y, 5)
        self.assertEqual(command.rover.orientation, 'N')

        command.Parse('FFFLBBBRFR')
        self.assertEqual(command.rover.orientation, 'E')
        self.assertEqual(command.rover.x, 6)
        self.assertEqual(command.rover.y, 9)

    def testWithoutInit(self):
        cmd = 'FFFLBBBRFR'
        try:
            Command(cmd)
        except Exception as e:
            self.assertIsNotNone(e)

    def testOutField(self):
        cmd = 'I 10 8;V 3 5 N'
        command = Command(cmd)
        self.assertEqual(command.field.X, 10)
        self.assertEqual(command.field.Y, 8)
        self.assertEqual(command.rover.x, 3)
        self.assertEqual(command.rover.y, 5)
        self.assertEqual(command.rover.orientation, 'N')
        try:
            command.Parse('FFFLBBBRFR')
        except Exception as e:
            self.assertIsNotNone(e)
        self.assertEqual(command.rover.orientation, 'N')
        self.assertEqual(command.rover.x, 6)
        self.assertEqual(command.rover.y, 8)

    def testSetObstacle(self):
        cmd = 'I 10 8;O 5 3;O 0 0;V 5 2 N'
        command = Command(cmd)
        self.assertRaises(
            MeetObstacleException,
            command.Parse,
            'FFFLBBBRFR'
        )
        self.assertEqual(command.rover.x, 5)
        self.assertEqual(command.rover.y, 2)


if __name__ == '__main__':
    unittest.main()
