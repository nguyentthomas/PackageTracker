import './App.css'
import React from 'react';
import { Admin, Resource} from "react-admin";
import dataProvider from "./dataProvider";
import Packages from "/components/Packages";
import PackageForm from "/components/PackageForm";

function App() {

  return (
    <>
    <Admin dataProvider={dataProvider} >
    <Resource name="packages" list={Packages} create={PackageForm}/>
    </Admin>
    </>
  )
}

export default App
