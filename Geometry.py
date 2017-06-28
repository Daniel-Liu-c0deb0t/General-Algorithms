from math import isclose, radians, degrees, sin, cos, acos, atan2

# point: (x, y, ...)
# line (ax + by + c = 0): (a, b, c) or 2 points
# line segment: 2 points
# vector: (x, y, ...)
# circle: point and radius
# triangle: 3 points, sometimes duplicate first point as last
# polygon: n points, duplicate first point as last


def points_equals(*points):
    for i in range(len(points) - 1):
        for j in range(len(points[i])):
            if not isclose(points[i][j], points[i + 1][j]):
                return False
    return True

print(points_equals((2, 4), (2, 4), (2.0, 4.0)))


def points_dist(point1, point2):
    dist_squared = 0
    for i in range(len(point1)):
        dist_squared += (point1[i] - point2[i]) ** 2
    return dist_squared ** 0.5

print(points_dist((0, 0, 0), (1, 1, 1)))


def point_rotate_2d(point, origin, theta):
    rad = radians(theta)
    return origin[0] + (point[0] - origin[0]) * cos(rad) - (point[1] - origin[1]) * sin(rad), \
           origin[1] + (point[0] - origin[0]) * sin(rad) + (point[1] - origin[1]) * cos(rad)

print(point_rotate_2d((1, 0), (0, 0), 180))


def points_to_line_2d(point1, point2):
    if isclose(point1[0], point2[0]):
        return 1, 0, -point1[0]
    else:
        a = -(point1[1] - point2[1]) / (point1[0] - point2[0])
        return a, 1, -(a * point1[0]) - point1[1]

print(points_to_line_2d((0, 1), (1, 1)))


def lines_parallel_2d(*lines):
    for i in range(len(lines) - 1):
        for j in range(len(lines[i]) - 1):
            if not isclose(lines[i][j], lines[i + 1][j]):
                return False
    return True

print(lines_parallel_2d(points_to_line_2d((0, 1), (1, 1)), points_to_line_2d((0, 0), (1, 0))))


def lines_equals_2d(*lines):
    for i in range(len(lines) - 1):
        for j in range(len(lines[i])):
            if not isclose(lines[i][j], lines[i + 1][j]):
                return False
    return True

print(lines_equals_2d(points_to_line_2d((0, 1), (1, 1)), points_to_line_2d((0, 1), (1, 1))))


def lines_intersect_2d(line1, line2):
    if lines_parallel_2d(line1, line2):
        return None
    x = (line2[1] * line1[2] - line1[1] * line2[2]) / (line2[0] * line1[1] - line1[0] * line2[1])
    if isclose(line1[1], 0):
        y = -(line2[0] * x + line2[2])
    else:
        y = -(line1[0] * x + line1[2])
    return x, y

print(lines_intersect_2d(points_to_line_2d((0, 1), (1, 1)), points_to_line_2d((1, 0), (1, 1))))


def line_line_seg_intersect_2d(line1, seg_point1, seg_point2):
    result = lines_intersect_2d(line1, points_to_line_2d(seg_point1, seg_point2))
    if result is None:
        return None
    x, y = result
    if x > max(seg_point1[0], seg_point2[0]) or x < min(seg_point1[0], seg_point2[0]):
        return None
    if y > max(seg_point1[1], seg_point2[1]) or y < min(seg_point1[1], seg_point2[1]):
        return None
    return result

print(line_line_seg_intersect_2d(points_to_line_2d((0, 1), (1, 1)), (1, 0), (1, 0.5)))


def line_seg_intersect_2d(seg_point1, seg_point2, seg_point3, seg_point4):
    result = lines_intersect_2d(points_to_line_2d(seg_point1, seg_point2), points_to_line_2d(seg_point3, seg_point4))
    if result is None:
        return None
    x, y = result
    if x > max(seg_point1[0], seg_point2[0]) or x < min(seg_point1[0], seg_point2[0]):
        return None
    if y > max(seg_point1[1], seg_point2[1]) or y < min(seg_point1[1], seg_point2[1]):
        return None
    if x > max(seg_point3[0], seg_point4[0]) or x < min(seg_point3[0], seg_point4[0]):
        return None
    if y > max(seg_point3[1], seg_point4[1]) or y < min(seg_point3[1], seg_point4[1]):
        return None
    return result

print(line_seg_intersect_2d((0, 1), (1, 2), (1, 1), (1, 2)))


def points_to_vector(point1, point2):
    return tuple([point2[i] - point1[i] for i in range(len(point1))])

print(points_to_vector((0, 0), (1, 1)))


def vector_scale(vector, scalar):
    return tuple([vector[i] * scalar for i in range(len(vector))])

print(vector_scale((1, 1), 5))


def point_translate(point, vector):
    return tuple([point[i] + vector[i] for i in range(len(point))])

print(point_translate((1, 1), (5, 5)))


def vectors_dot(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    return result

print(vectors_dot((1, 2, 3), (4, 5, 6)))


def vector_normal_squared(vector):
    result = 0
    for i in vector:
        result += i ** 2
    return result

print(vector_normal_squared((1, 1)))


def point_dist_to_line(point, line_point1, line_point2):
    vector1 = points_to_vector(line_point1, point)
    vector2 = points_to_vector(line_point1, line_point2)
    point_on_line = point_translate(line_point1, vector_scale(vector2, vectors_dot(vector1, vector2) /
                                                              vector_normal_squared(vector2)))
    return points_dist(point, point_on_line), point_on_line

print(point_dist_to_line((0, 0), (0, 1), (1, 2)))


def point_dist_to_line_seg(point, seg_point1, seg_point2):
    vector1 = points_to_vector(seg_point1, point)
    vector2 = points_to_vector(seg_point1, seg_point2)
    u = vectors_dot(vector1, vector2) / vector_normal_squared(vector2)
    if u < 0:
        return points_dist(point, seg_point1), seg_point1
    if u > 1:
        return points_dist(point, seg_point2), seg_point2
    point_on_line = point_translate(seg_point1, vector_scale(vector2, u))
    return points_dist(point, point_on_line), point_on_line

print(point_dist_to_line_seg((0, 0, 0), (0, 1, 0), (1, 1, 0)))


def points_to_angle_2d(point1, point2, point3):
    vector1 = points_to_vector(point2, point1)
    vector2 = points_to_vector(point2, point3)
    return degrees(acos(vectors_dot(vector1, vector2) /
                        (vector_normal_squared(vector1) * vector_normal_squared(vector2)) ** 0.5))

print(points_to_angle_2d((1, 0), (0, 0), (1, 1)))


def vectors_cross_2d(vector1, vector2):
    return vector1[0] * vector2[1] - vector1[1] * vector2[0]

print(vectors_cross_2d((1, 1), (2, 3)))


def points_ccw_2d(point1, point2, point3):
    return vectors_cross_2d(points_to_vector(point1, point2), points_to_vector(point1, point3)) >= 0

print(points_ccw_2d((0, 0), (0.5, 0.5), (-1, 1)))


def points_collinear_2d(point1, point2, point3):
    return isclose(vectors_cross_2d(points_to_vector(point1, point2), points_to_vector(point1, point3)), 0)

print(points_collinear_2d((0, 0), (1, 1), (3, 4)))


def point_inside_circle(point, center, radius):
    d = points_to_vector(center, point)
    dist = vector_normal_squared(d)
    r = radius ** len(point)
    return dist <= r

print(point_inside_circle((0, 0), (1, 1), 1.5))


def perimeter_2d(points):
    result = 0
    for i in range(len(points) - 1):
        result += points_dist(points[i], points[i + 1])
    return result

print(perimeter_2d(((0, 0), (0, 1), (1, 2), (2, 2), (0, 0))))


def area_2d(points):
    result = 0
    for i in range(len(points) - 1):
        result += points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
    return abs(result / 2)

print(area_2d(((0, 0), (0, 2), (2, 2), (2, 0), (0, 0))))


def triangle_incircle_2d(point1, point2, point3):
    radius = area_2d((point1, point2, point3, point1)) / (perimeter_2d((point1, point2, point3, point1)) / 2)
    if isclose(radius, 0):
        return None
    ratio1 = points_dist(point1, point2) / points_dist(point1, point3)
    p1 = point_translate(point2, vector_scale(points_to_vector(point2, point3), ratio1 / (1 + ratio1)))
    line1 = points_to_line_2d(point1, p1)
    ratio2 = points_dist(point2, point1) / points_dist(point2, point3)
    p2 = point_translate(point1, vector_scale(points_to_vector(point1, point3), ratio2 / (1 + ratio2)))
    line2 = points_to_line_2d(point2, p2)
    return lines_intersect_2d(line1, line2), radius

print(triangle_incircle_2d((0, 2), (0, 0), (2, 0)))


def triangle_circumcircle_radius_2d(point1, point2, point3):
    return points_dist(point1, point2) * points_dist(point2, point3) * points_dist(point3, point1) / \
           (4 * area_2d((point1, point2, point3, point1)))

print(triangle_circumcircle_radius_2d((0, 2), (0, 0), (2, 0)))


def is_convex_2d(points):
    if len(points) <= 3:
        return False
    is_left = points_ccw_2d(points[0], points[1], points[2])
    for i in range(1, len(points) - 1):
        if points_ccw_2d(points[i], points[i + 1], points[1 if i + 2 == len(points) else i + 2]) != is_left:
            return False
    return True

print(is_convex_2d(((1, 0), (1, 1), (0.7, 0.5), (0, 0), (1, 0))))


def point_inside_2d(point, points):
    if len(points) == 0:
        return False
    total = 0
    for i in range(len(points) - 1):
        if points_equals(point, points[i]) or points_equals(point, points[i + 1]):
            return True
        if points_ccw_2d(point, points[i], points[i + 1]):
            total += points_to_angle_2d(points[i], point, points[i + 1])
        else:
            total -= points_to_angle_2d(points[i], point, points[i + 1])
    return isclose(abs(total) - 360, 0)

print(point_inside_2d((0.8, 0.5), ((1, 0), (1, 1), (0.7, 0.5), (0, 0), (1, 0))))


def graham_scan_2d(points):
    if len(points) <= 3:
        if points[0] != points[-1]:
            points.append(points[0])
        return points
    min_y = points[0][1]
    min_i = 0
    for i in range(1, len(points)):
        if points[i][1] < min_y or (points[i][1] == min_y and points[i][0] < points[min_i][0]):
            min_y = points[i][1]
            min_i = i
    points[0], points[min_i] = points[min_i], points[0]
    pivot = points[0]
    points.sort(key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]), points_dist(pivot, p)))
    stack = [points[-1], points[0], points[1]]
    i = 2
    while i < len(points):
        j = len(stack) - 1
        if not points_ccw_2d(points[i], stack[j], stack[j - 1]):
            stack.append(points[i])
            i += 1
        else:
            stack.pop()
    return stack

print(graham_scan_2d([(0, 0), (1, 1), (2, 1), (3, 0), (3, -1), (2, -2), (1, -2), (0, -1), (0.5, 0.5)]))
