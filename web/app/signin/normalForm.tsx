"use client";
import React, { useEffect, useReducer, useState } from "react";
import { useRouter } from "next/navigation";
import { IS_CE_EDITION } from "@/config";
import classNames from "classnames";
import useSWR from "swr";
import Link from "next/link";
import style from "./page.module.css";
import Toast from "../components/base/toast";
