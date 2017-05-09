import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (lines, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for line in lines:
        command = line[0]
        args = line[1:]

        if command == 'line':
            add_edge(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
        
        elif command == 'circle':
            add_circle(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), step)
        
        elif command == 'hermite' or command == 'bezier':
            add_curve(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), step, command)
        
        elif command == 'box':
            add_box(tmp, float(args[0]),float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, color)
            tmp = []
        
        elif command == 'sphere':
            add_sphere(tmp,float(args[0]), float(args[1]), float(args[2]), float(args[3]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        
        elif command == 'torus':
            add_torus(tmp, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif command == 'scale':
            s = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], s )
            stack[-1] = [ i[:] for i in s]
        elif command == 'move':
            m = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], m )
            stack[-1] = [ i[:] for i in m]
        elif command == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                r = make_rotX(theta)
            elif args[0] == 'y':
                r = make_rotY(theta)
            else:
                r = make_rotZ(theta)
                matrix_mult( stack[-1], r )
                stack[-1] = [ i[:] for i in r]
        elif command == 'clear':
            tmp = []
        elif command == 'ident':
            ident(transform)
        elif command == 'apply':
            matrix_mult(transform, tmp)
        elif command == 'push':
            stack.append( [ i[:] for i in stack[-1]])
        elif command == 'pop':
            stack.pop()
        elif command == 'display' or command == 'save':
            if command == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])

        print command
