import unittest
from Field import Field
from Location import *
from Rover import Rover
from Command import Command
from Errors import *
class testCases(unittest.TestCase):
    def testLocation(self):
        location = Location(3,5)
        self.assertEqual(location.x,3)
        self.assertEqual(location.y,5)
        self.assertEqual(xPlus(location), Location(4, 5))
        self.assertEqual(xMinus(location),Location(2,5))
        self.assertEqual(yPlus(location), Location(3, 6))
        self.assertEqual(yMinus(location),Location(3,4))

    def testField(self):
        field = Field(Location(0,0),Location(100,100))
        field.setObstacles((5,3),(0,0))
        self.assertFalse(field.isObstacle(Location(0,1)))
        self.assertTrue(field.isObstacle(Location(5,3)))
        self.assertRaises(
            OutFieldError,
            field.setObstacles,
            (-1, 0)
        )


    def testRover(self):
        rover = Rover(Location(3,5),Orientation('N'))
        self.assertEqual(rover.location.x,3)
        self.assertEqual(rover.location.y,5)
        self.assertEqual(rover.orientation,Orientation('N'))

    def testMove(self):
        rover = Rover(Location(3, 5), Orientation('N'))
        field = Field(Location(0, 0), Location(100, 100))
        rover.moveForward(field)
        self.assertEqual(rover.location.x, 3)
        self.assertEqual(rover.location.y, 6)
        self.assertEqual(rover.orientation, Orientation('N'))
        rover.moveBack(field)
        self.assertEqual(rover.location.y, 5)

        rover = Rover(Location(3, 5), Orientation('W'))
        rover.moveForward(field)
        self.assertEqual(rover.location.x, 2)
        self.assertEqual(rover.location.y, 5)

    def testTurn(self):
        rover = Rover(Location(3, 5), Orientation('N'))
        field = Field(Location(0, 0), Location(100, 100))
        rover.turnLeft(field)
        self.assertEqual(rover,Rover(Location(3,5),Orientation('W')))

        rover = Rover(Location(3, 5), Orientation('E'))
        rover.turnLeft(field)
        self.assertEqual(rover, Rover(Location(3, 5), Orientation('N')))

        rover = Rover(Location(3, 5), Orientation('N'))
        rover.turnRight(field)
        self.assertEqual(rover, Rover(Location(3, 5), Orientation('E')))


    def testCommand(self):
        cmd = 'I 0,0 40,40;'
        command = Command(cmd)
        self.assertEqual(command.field, Field(Location(0, 0),Location(40,40)))
        cmd = 'O 5,3'
        command.Parse(cmd)
        self.assertEqual(command.field.obstacles,[(5,3)])
        cmd = 'V 2,1 N'
        command.Parse(cmd)
        self.assertEqual(command.rover.location.x,2)
        self.assertEqual(command.rover.location.y,1)
        self.assertEqual(command.rover.orientation,Orientation('N'))

    def testCommandMove(self):
        cmd = 'I 0,0 40,40;V 2,1 N'
        command = Command(cmd)
        self.assertEqual(command.field, Field(Location(0, 0), Location(40, 40)))
        self.assertEqual(command.rover.location.x, 2)
        self.assertEqual(command.rover.location.y, 1)
        self.assertEqual(command.rover.orientation, Orientation('N'))
        move = 'FFFLBBBRF'
        command.Parse(move)
        self.assertEqual(command.rover.location.x, 5)
        self.assertEqual(command.rover.location.y, 5)
        self.assertEqual(command.rover.orientation, Orientation('N'))

    def testWrongMove(self):
        cmd = 'I 0,0 10,10;V 2,1 N;O 2,3 6,6'
        command = Command(cmd)
        move = 'FFFLBBBRF'
        try:
            command.Parse(move)
        except Exception as e:
            print(e)
        self.assertEqual(command.rover.location.x, 2)
        self.assertEqual(command.rover.location.y, 2)
        self.assertEqual(command.rover.orientation, Orientation('N'))

    def testWrongMove2(self):
        cmd = 'I 0,0 10,10;V 2,1 N;'
        command = Command(cmd)
        move = 'FFFFFFFFFFFF'
        try:
            command.Parse(move)
        except Exception as e:
            print(e)
        self.assertEqual(command.rover.location.x, 2)
        self.assertEqual(command.rover.location.y, 10)
        self.assertEqual(command.rover.orientation, Orientation('N'))


if __name__ == '__main__':
    unittest.main()
