import './App.css'
import React from 'react';
import { Admin, Resource} from "react-admin";
import dataProvider from "./dataProvider";
import Packages from "/components/Packages";

function App() {

  return (
    <>
    <Admin dataProvider={dataProvider} >
    <Resource name="packages" list={Packages} />
    </Admin>
    </>
  )
}

export default App
