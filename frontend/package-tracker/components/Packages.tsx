import { useEffect, useState, useRef, useCallback } from "react";
import { List, Datagrid, TextField, EditButton, DeleteButton, Pagination } from "react-admin";
import React from "react";

const PostPagination = () => <Pagination rowsPerPageOptions={[10, 25, 50, 100]} />;

export default function Packages() {

  return (
    <>
      <List pagination={<PostPagination/>}>
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