/*
    Copyright 2008 Wolfgang Ginolas
    Copyright 2023-2025 Nikolay Borodin <Monsterovich>

    This file is part of Lanemu.

    Lanemu is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Lanemu is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Lanemu.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <jni.h>

#ifndef TUNTAP_H
#define TUNTAP_H

#define JFUNC(type, name, ...) JNIEXPORT type JNICALL Java_org_p2pvpn_tuntap_TunTapWindows_##name (JNIEnv *env, jobject this, ##__VA_ARGS__)

JFUNC(jint, openTun);
JFUNC(void, close);
JFUNC(void, write, jbyteArray, jint);
JFUNC(jint, read, jbyteArray);

#endif
