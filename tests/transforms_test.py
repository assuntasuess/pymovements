# Copyright (c) 2022-2023 The pymovements Project Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Test all functions in pymovements.transforms.
"""
import numpy as np
import pytest

from pymovements.transforms import norm
from pymovements.transforms import pix2deg
from pymovements.transforms import pos2vel
from pymovements.transforms import split

n_coords = 100
screen_px_1d = 100
screen_cm_1d = 100
screen_px_2d = [100, 100]
screen_cm_2d = [100, 100]


@pytest.mark.parametrize(
explicetly    'kwargs, expected_error, exp_err_msg',
    [
        pytest.param(
            {
                'arr': None,
                'screen_px': 1,
                'screen_cm': 1,
                'distance_cm': 1,
                'origin': 'center',
            },
            TypeError,
            'arr must not be None',
            id='none_coords_raises_type_error',
        ),
        pytest.param(
            {
                'arr': 0,
                'screen_px': None,
                'screen_cm': 1,
                'distance_cm': 1,
                'origin': 'center',
            },
            TypeError,
            "unsupported operand type(s) for /: 'NoneType' and 'int'",
            id='none_screen_px_raises_type_error',
        ),
        pytest.param(
            {
                'arr': 0,
                'screen_px': 1,
                'screen_cm': None,
                'distance_cm': 1,
                'origin': 'center',
            },
            TypeError,
            "unsupported operand type(s) for /: 'int' and 'NoneType'",
            id='none_screen_cm_raises_type_error',
        ),
        pytest.param(
            {
                'arr': 0,
                'screen_px': 1,
                'screen_cm': 1,
                'distance_cm': None,
                'origin': 'center',
            },
            TypeError,
            "unsupported operand type(s) for *: 'NoneType' and 'float'",
            id='none_distance_cm_raises_type_error',
        ),
        pytest.param(
            {
                'arr': 0,
                'screen_px': 0,
                'screen_cm': 1,
                'distance_cm': 1,
                'origin': 'center',
            },
            ValueError,
            'screen_px must not be zero',
            id='zero_screen_px_raises_value_error',
        ),
        pytest.param(
            {
                'arr': 0,
                'screen_px': 1,
                'screen_cm': 0,
                'distance_cm': 1,
                'origin': 'center',
            },
            ValueError,
            'screen_cm must not be zero',
            id='zero_screen_cm_raises_value_error',
        ),
        pytest.param(
            {
                'arr': 0,
                'screen_px': 1,
                'screen_cm': 1,
                'distance_cm': 0,
                'origin': 'center',
            },
            ValueError,
            'distance_cm must not be zero',
            id='zero_distance_cm_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.zeros((10, 2, 2)),
                'screen_px': screen_px_2d,
                'screen_cm': screen_cm_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'Number of dimensions of arr must be either 0, 1 or 2 (arr.ndim: 3)',
            id='rank_3_tensor_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [[0, 0]] * n_coords,
                'screen_px': screen_px_1d,
                'screen_cm': screen_px_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'arr is 2-dimensional, but screen_px is not',
            id='list_coords_2d_screen_px_1d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [[0, 0]] * n_coords,
                'screen_px': screen_px_2d,
                'screen_cm': screen_px_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'arr is 2-dimensional, but screen_cm is not',
            id='list_coords_2d_screen_cm_1d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [0] * n_coords,
                'screen_px': screen_px_2d,
                'screen_cm': screen_px_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'arr is 1-dimensional, but screen_px is not',
            id='list_coords_1d_screen_px_2d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [0] * n_coords,
                'screen_px': screen_px_1d,
                'screen_cm': screen_px_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'arr is 1-dimensional, but screen_cm is not',
            id='list_coords_1d_screen_cm_2d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.zeros((n_coords, 3)),
                'screen_px': [1, 1, 1],
                'screen_cm': [1, 1, 1],
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'Last coord dimension must have length 1, 2 or 4. (arr.shape: (100, 3))',
            id='list_coords_3d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.zeros((n_coords, 4)),
                'screen_px': screen_px_1d,
                'screen_cm': screen_px_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'arr is 4-dimensional, but screen_px is not 2-dimensional',
            id='list_coords_4d_screen_px_not_2d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.zeros((n_coords, 4)),
                'screen_px': screen_px_2d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            ValueError,
            'arr is 4-dimensional, but screen_cm is not 2-dimensional',
            id='list_coords_4d_screen_cm_not_2d_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.zeros((n_coords, 4)),
                'screen_px': screen_px_2d,
                'screen_cm': screen_px_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'invalid',
            },
            ValueError,
            'origin invalid is not supported.',
            id='invalid_origin_str_raises_value_error',
        ),
    ],
)
def test_pix2deg_raises_error(kwargs, expected_error, exp_err_msg):
    with pytest.raises(expected_error) as error_info:
        pix2deg(**kwargs)
    actual_msg, = error_info.value.args
    assert actual_msg == exp_err_msg


@pytest.mark.parametrize(
    'kwargs, expected_value',
    [
        pytest.param(
            {
                'arr': 0,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            0,
            id='zero_coord_without_center_origin_returns_zero',
        ),
        pytest.param(
            {
                'arr': (screen_px_1d - 1) / 2,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'lower left',
            },
            0,
            id='center_coord_with_center_origin_returns_zero',
        ),
        pytest.param(
            {
                'arr': screen_px_1d / 2,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2,
                'origin': 'center',
            },
            45,
            id='isosceles_triangle_without_center_origin_returns_45',
        ),
        pytest.param(
            {
                'arr': screen_px_1d - 0.5,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2,
                'origin': 'lower left',
            },
            45,
            id='isosceles_triangle_with_center_origin_returns_45',
        ),
        pytest.param(
            {
                'arr': -0.5,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2,
                'origin': 'lower left',
            },
            -45,
            id='isosceles_triangle_left_with_center_origin_returns_minus45',
        ),
        pytest.param(
            {
                'arr': screen_px_2d[0] / 2 * np.ones((n_coords, 2)),
                'screen_px': screen_px_2d,
                'screen_cm': screen_cm_2d,
                'distance_cm': screen_px_2d[0] / 2,
                'origin': 'center',
            },
            45,
            id='nparray_of_isosceles_triangle_without_center_origin_returns_45',
        ),
        pytest.param(
            {
                'arr': screen_px_1d / 2,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            pytest.approx(26.565, abs=1e-4),
            id='ankathet_half_without_center_origin_returns_26565',
        ),
        pytest.param(
            {
                'arr': screen_px_1d - 0.5,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'lower left',
            },
            pytest.approx(26.565, abs=1e-4),
            id='ankathet_half_with_center_origin_returns_26565',
        ),
        pytest.param(
            {
                'arr': screen_px_1d / 2,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2 / np.sqrt(3),
                'origin': 'center',
            },
            pytest.approx(60),
            id='ankathet_sqrt_3_without_center_origin_returns_60',
        ),
        pytest.param(
            {
                'arr': screen_px_1d - 0.5,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2 / np.sqrt(3),
                'origin': 'lower left',
            },
            pytest.approx(60),
            id='ankathet_sqrt_3_with_center_origin_returns_60',
        ),
        pytest.param(
            {
                'arr': screen_px_1d / 2,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2 * np.sqrt(3),
                'origin': 'center',
            },
            pytest.approx(30),
            id='opposite_sqrt_3_without_center_origin_returns_30',
        ),
        pytest.param(
            {
                'arr': screen_px_1d - 0.5,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d / 2 * np.sqrt(3),
                'origin': 'lower left',
            },
            pytest.approx(30),
            id='opposite_sqrt_3_with_center_origin_returns_30',
        ),
        pytest.param(
            {
                'arr': [0] * n_coords,
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            np.array([0.0] * n_coords),
            id='list_of_zero_coords_1d',
        ),
        pytest.param(
            {
                'arr': np.array([0] * n_coords),
                'screen_px': screen_px_1d,
                'screen_cm': screen_cm_1d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            np.array([0.0] * n_coords),
            id='nparray_of_zero_coords_1d',
        ),
        pytest.param(
            {
                'arr': [[0, 0]] * n_coords,
                'screen_px': screen_px_2d,
                'screen_cm': screen_cm_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            np.array([[0.0, 0.0]] * n_coords),
            id='list_of_zero_coords_2d',
        ),
        pytest.param(
            {
                'arr': np.array([[0, 0]] * n_coords),
                'screen_px': screen_px_2d,
                'screen_cm': screen_cm_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            np.array([[0.0, 0.0]] * n_coords),
            id='nparray_of_zero_coords_2d',
        ),
        pytest.param(
            {
                'arr': np.array([[0.0, 0.0, 0.0, 0.0]] * n_coords),
                'screen_px': screen_px_2d,
                'screen_cm': screen_cm_2d,
                'distance_cm': screen_cm_1d,
                'origin': 'center',
            },
            np.array([[0.0, 0.0, 0.0, 0.0]] * n_coords),
            id='nparray_of_zero_coords_4d',
        ),
    ],
)
def test_pix2deg_returns(kwargs, expected_value):
    actual_value = pix2deg(**kwargs)
    assert (actual_value == expected_value).all()


@pytest.mark.parametrize(
    'kwargs, expected_error, exp_err_msg',
    [
        pytest.param(
            {
                'arr': [[0] * 10],
                'sampling_rate': 0,
            },
            ValueError,
            'sampling_rate needs to be above zero',
            id='sampling_rate_zero_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [[0] * 10],
                'sampling_rate': -1,
            },
            ValueError,
            'sampling_rate needs to be above zero',
            id='sampling_rate_less_zero_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [0] * 5,
                'method': 'smooth',
            },
            ValueError,
            'arr has to have at least 6 elements for method "smooth"',
            id='list_length_below_six_method_smooth_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [0] * 2,
                'method': 'neighbors',
            },
            ValueError,
            'arr has to have at least 3 elements for method "neighbors"',
            id='list_length_below_three_method_neighbors_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [0],
                'method': 'preceding',
            },
            ValueError,
            'arr has to have at least 2 elements for method "preceding"',
            id='list_length_below_two_method_preceding_raises_value_error',
        ),
        pytest.param(
            {
                'arr': [0] * 10,
                'method': 'invalid',
            },
            ValueError,
            "Method needs to be in ['smooth', 'neighbors', 'preceding', 'savitzky_golay'] "
            "(is: invalid)",
            id='invalid_method_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.ones((3, 3, 3)),
                'method': 'smooth',
            },
            ValueError,
            'arr needs to have 1 or 2 dimensions (arr dimensions are: 3)',
            id='wrong_dimensions_input_arr_raises_value_error',
        ),
        pytest.param(
            {
                'arr': np.ones(10),
                'method': 'smooth',
                'kwargs': {},
            },
            ValueError,
            "selected method doesn't support any additional kwargs",
            id='kwargs_passed_but_method_not_savitzky_golay_raises_value_error',
        ),
    ],
)
def test_pos2vel_raises_error(kwargs, expected_error, exp_err_msg):
    with pytest.raises(expected_error) as error_info:
        pos2vel(**kwargs)
    actual_err_msg, = error_info.value.args
    assert actual_err_msg == exp_err_msg


@pytest.mark.parametrize(
    'method',
    [
        pytest.param('smooth', id='method_smooth'),
        pytest.param('neighbors', id='method_neighbors'),
        pytest.param('preceding', id='method_preceding'),
    ],
)
@pytest.mark.parametrize(
    'kwargs, padding, expected_value',
    [
        pytest.param(
            {
                'arr': np.repeat(0, n_coords),
                'sampling_rate': 1,
            },
            (0, n_coords),
            np.zeros(n_coords),
            id='constant_input_returns_zero_velocity',
        ),
        pytest.param(
            {
                'arr': np.linspace(0, n_coords - 1, n_coords),
                'sampling_rate': 1,
            },
            (1, -1),
            np.ones(n_coords),
            id='linear_input_returns_constant_velocity',
        ),
    ],
)
def test_pos2vel_returns(method, kwargs, padding, expected_value):
    actual_value = pos2vel(method=method, **kwargs)
    assert (actual_value[padding[0]:padding[1]] == expected_value[padding[0]:padding[1]]).all()


@pytest.mark.parametrize(
    'params, expected_value',
    [
        pytest.param(
            {'method': 'preceding', 'sampling_rate': 1},
            np.array([2.0, 0.0] * (100 // 2)),
            id='method_preceding_alternating_velocity',
        ),
        pytest.param(
            {'method': 'neighbors', 'sampling_rate': 1},
            np.ones((100,)),
            id='method_neighbors_linear_velocity',
        ),
        pytest.param(
            {'method': 'smooth', 'sampling_rate': 1},
            np.ones((100,)),
            id='method_smooth_linear_velocity',
        ),
        pytest.param(
            {'method': 'savitzky_golay', 'window_length': 7, 'polyorder': 2, 'sampling_rate': 1},
            np.concatenate([
                np.array([0.71428571, 0.80952381, 0.9047619]),
                np.ones((94,)),
                np.array([0.9047619, 0.80952381, 0.71428571]),
            ]),
            id='method_savitzky_golay_linear_velocity',
        ),
    ],
)
def test_pos2vel_stepped_input_returns(params, expected_value):
    N = 100
    x = np.linspace(0, N - 2, N // 2)
    x = np.repeat(x, 2)

    actual_value = pos2vel(x, **params)

    lpad, rpad = 1, -1
    assert np.allclose(actual_value[lpad:rpad], expected_value[lpad:rpad])


@pytest.mark.parametrize(
    'params, expected_value',
    [
        pytest.param(
            {'method': 'savitzky_golay', 'window_length': 7, 'polyorder': 2, 'sampling_rate': 1},
            np.concatenate([
                np.array([
                    [0.71428571, 0.71428571],
                    [0.80952381, 0.80952381],
                    [0.9047619, 0.9047619],
                ]),
                np.ones((94, 2)),
                np.array([
                    [0.9047619, 0.9047619],
                    [0.80952381, 0.80952381],
                    [0.71428571, 0.71428571],
                ]),
            ]),
            id='method_savitzky_golay_linear_velocity_2d_input',
        ),
    ],
)
def test_pos2vel_2d_stepped_input_returns(params, expected_value):
    N = 100
    x = np.linspace(0, N - 2, N // 2)
    x = np.repeat(x, 4)
    x = np.reshape(x, (100, 2))

    actual_value = pos2vel(x, **params)

    lpad, rpad = 1, -1
    assert np.allclose(actual_value[lpad:rpad], expected_value[lpad:rpad])


@pytest.mark.parametrize(
    'params, expected_value',
    [
        pytest.param(
            {'arr': np.ones((2, 2, 5)), 'axis': None},
            np.array([
                [1.41421356, 1.41421356, 1.41421356, 1.41421356, 1.41421356],
                [1.41421356, 1.41421356, 1.41421356, 1.41421356, 1.41421356],
            ]),
            id='3_dim_array_no_axis',
        ),
        pytest.param(
            {'arr': np.ones((2, 5)), 'axis': None},
            np.array([[1.41421356, 1.41421356, 1.41421356, 1.41421356, 1.41421356]]),
            id='2_dim_array_no_axis',
        ),
        pytest.param(
            {'arr': np.ones((2, 2, 2, 2)), 'axis': 2},
            np.array([
                [
                    [1.41421356, 1.41421356],
                    [1.41421356, 1.41421356],
                ],
                [
                    [1.41421356, 1.41421356],
                    [1.41421356, 1.41421356],
                ],
            ]),
            id='4_dim_array_with_axis',
        ),
    ],
)
def test_norm(params, expected_value):
    actual_value = norm(**params)
    assert np.allclose(actual_value, expected_value)


@pytest.mark.parametrize(
    'params, expected_error, exp_err_msg',
    [
        pytest.param(
            {'arr': np.ones((2, 2, 5, 5)), 'axis': None},
            ValueError,
            'Axis can not be inferred in case of more than 3 input array dimensions '
            '(arr.shape=(2, 2, 5, 5)). Either reduce the number of input array dimensions '
            'or specify `axis` explicitly.',
            id='4_dim_array_no_axis_raises_value_error',
        ),
    ],
)
def test_norm_raises_exception(params, expected_error, exp_err_msg):
    with pytest.raises(expected_error) as error_info:
        norm(**params)
    actual_msg, = error_info.value.args
    assert actual_msg == exp_err_msg


@pytest.mark.parametrize(
    'params, expected',
    [
        pytest.param(
            {'arr': np.ones((1, 10, 2)), 'window_size': 2, 'keep_padded': False},
            {'value': np.ones((5, 2, 2))},
            id='length_double_window_size2_keep_padded_returns_two_instances',
        ),
        pytest.param(
            {'arr': np.ones((1, 10, 2)), 'window_size': 5, 'keep_padded': False},
            {'value': np.ones((2, 5, 2))},
            id='length_double_window_size_keep_padded_returns_two_instances',
        ),
        pytest.param(
            {'arr': np.ones((1, 10, 2)), 'window_size': 5, 'keep_padded': True},
            {'value': np.ones((2, 5, 2))},
            id='length_double_window_size_not_keep_padded_returns_two_instances',
        ),
        pytest.param(
            {'arr': np.ones((1, 11, 2)), 'window_size': 5, 'keep_padded': False},
            {'value': np.ones((2, 5, 2))},
            id='length_double_window_size+1_keep_padded_returns_two_instances',
        ),
        pytest.param(
            {'arr': np.ones((1, 11, 2)), 'window_size': 5, 'keep_padded': True},
            {
                'value': np.concatenate([
                    np.ones((2, 5, 2)),
                    np.expand_dims(np.concatenate([np.ones((1, 2)), np.ones((4, 2)) * np.nan]), 0),
                ]),
            },
            id='length_double_window_size+1_not_keep_padded_returns_three_instances',
        ),
        pytest.param(
            {'arr': np.ones((2, 10, 2)), 'window_size': 5, 'keep_padded': False},
            {'value': np.ones((4, 5, 2))},
            id='two_instances_length_double_window_size_keep_padded_returns_two_instances',
        ),
        pytest.param(
            {'arr': np.ones((2, 11, 2)), 'window_size': 5, 'keep_padded': True},
            {
                'value': np.concatenate([
                    np.ones((2, 5, 2)),
                    np.expand_dims(np.concatenate([np.ones((1, 2)), np.ones((4, 2)) * np.nan]), 0),
                    np.ones((2, 5, 2)),
                    np.expand_dims(np.concatenate([np.ones((1, 2)), np.ones((4, 2)) * np.nan]), 0),
                ]),
            },
            id='two_instances_length_double_window_size+1_not_keep_padded_returns_six_instances',
        ),
    ],
)
def test_cut_into_subsequences(params, expected):
    if 'exception' in expected:
        with pytest.raises(expected['exception']):
            split(**params)
        return

    arr = split(**params)

    assert np.array_equal(arr, expected['value'], equal_nan=True), (
        f"arr = {arr}, expected = {expected['value']}"
    )
