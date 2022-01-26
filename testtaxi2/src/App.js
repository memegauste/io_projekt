import './App.css';
import * as React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Card, Button, CardBody, CardTitle,CardText } from "reactstrap";
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

L.Icon.Default.imagePath = 'img/'

function App() {
  const position = [53.776, 20.480]

  return (
    <div>
      <MapContainer center={position} zoom={14} scrollWheelZoom={false} className='map'>
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={position}>
          <Popup>
            Przykładowy punkt docelowy kurła
          </Popup>
        </Marker>
      </MapContainer>
      <Card className= "orderList">
        <CardBody>
          <CardTitle tag="h1">
            Kierowcy
          </CardTitle>
          <CardText>
            LOREM IPSUM SMIECIU
          </CardText>
        </CardBody>
      </Card>
    </div>
  );
}

export default App;
