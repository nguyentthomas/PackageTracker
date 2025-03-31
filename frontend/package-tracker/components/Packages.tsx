import { useEffect, useState, useRef, useCallback } from "react";
import { List, Datagrid, TextField } from "react-admin";
import React from "react";

export default function Packages() {

  return (
    <>
      <List>
        <Datagrid rowClick="edit">
          <TextField source="PackageID" label="PackageID" />
        </Datagrid>

      </List>
    </>
  );
}