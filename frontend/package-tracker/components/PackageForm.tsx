import * as React from "react";
import { SimpleForm, TextInput, Create, DateInput, Button, SelectInput, minValue } from "react-admin";
export default function PackageForm() {
    return (
        <Create>
            <SimpleForm>
                <TextInput source="id" label="ID"/>
                <TextInput source="recipient" label="Recipient" />
                <TextInput source="sender" label="Sender" />
                <TextInput source="trackingReference" label="Tracking Reference" />
                <SelectInput source="deliveryType" label="Delivery Type" choices={[
                    { id: 'DELIVERY', name: 'Delivery' },
                    { id: 'RETURN', name: 'Return' },
                ]} />
                <TextInput source="item" label="Item" />
                <TextInput source="shippingMethod" label="Shipping Method" />
                <DateInput source="dateSent" label="Date Sent" validate={minValue(1970-12-12)} />
                <SelectInput source="status" label="Status" choices={[
                    { id: 'NOT SENT', name: 'Not Sent'  },
                    { id: 'IN TRANSIT', name: 'In Transit' },
                    { id: 'ARRIVED', name: 'Arrived' },
                    { id: 'COMPLETED', name: 'Completed' },
                ]} />
                <TextInput source="note" label="Note" />
            </SimpleForm>
        </Create>
    );
}