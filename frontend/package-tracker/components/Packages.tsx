import { useEffect, useState, useRef, useCallback } from "react";
import { List, Datagrid, TextField, EditButton, DeleteButton, SearchInput} from "react-admin";
import React from "react";

const filters = [
  <SearchInput source="id" alwaysOn />,
];

export default function Packages() {

  return (
    <>
      <List filters={filters}>
        <Datagrid rowClick="edit">
          <TextField source="id" label="ID" />
          <TextField source="recipient" label="Recipient" />
          <TextField source="sender" label="Sender" />
          <TextField source="trackingReference" label="Tracking Reference" />
          <TextField source="deliveryType" label="Delivery Type" />
          <TextField source="item" label="Item" />
          <TextField source="shippingMethod" label="Shipping Method" />
          <TextField source="dateSent" label="Date Sent" />
          <TextField source="status" label="Status" />
          <TextField source="note" label="Note" />
          <EditButton/>
          <DeleteButton/>
        </Datagrid>

      </List>
    </>
  );
}