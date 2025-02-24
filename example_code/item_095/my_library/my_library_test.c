/*
 * Copyright 2014-2024 Brett Slatkin, Pearson Education Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include "my_library.h"


int main(int argc, char** argv) {
    {
        double a[] = {3, 4, 5};
        double b[] = {-1, 9, -2.5};
        double found = dot_product(3, a, b);
        double expected = 20.5;
        printf("Found %f, Expected %f\n", found, expected);
        assert(fabs(found - expected) < 0.01);
    }

    {
        double a[] = {0, 0, 0};
        double b[] = {1, 1, 1};
        double found = dot_product(3, a, b);
        double expected = 0;
        printf("Found %f, Expected %f\n", found, expected);
        assert(fabs(found - expected) < 0.01);
    }

    {
        double a[] = {-1, -1, -1};
        double b[] = {1, 1, 1};
        double found = dot_product(3, a, b);
        double expected = -3;
        printf("Found %f, Expected %f\n", found, expected);
        assert(fabs(found - expected) < 0.01);
    }

    return 0;
}
