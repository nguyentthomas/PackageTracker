import * as React from "react";
import {SimpleForm, TextInput, Create, DateInput, Button } from "react-admin";

export default function PackageForm() {
    return (
        <Create>
            <SimpleForm>
                <TextInput source="id" label="ID" required  />
                <TextInput source="recipient" label="Recipient" />
                <TextInput source="sender" label="Sender" />
                <TextInput source="trackingReference" label="Tracking Reference" />
                <TextInput source="deliveryType" label="Delivery Type" />
                <TextInput source="item" label="Item" />
                <TextInput source="shippingMethod" label="Shipping Method" />
                <TextInput source="dateSent" label="Date Sent" />
                <TextInput source="status" label="Status" />
                <TextInput source="note" label="Note" />
            </SimpleForm>
        </Create>
    );
}