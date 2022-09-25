import 'leaflet/dist/leaflet.css';
import React, { useEffect, useState } from 'react';

import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import staticData from "../../data/outputs.json";

import L, { LatLngExpression } from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [17, 38]
});

L.Marker.prototype.options.icon = DefaultIcon;

const romeLocation: LatLngExpression = [41.9028, 12.4964];


export default function Map(): JSX.Element {
  const [markerList, setMarkerList] = useState([]);

  function isLocalHost(url: string) {
    return url.indexOf('localhost') !== -1 || url.indexOf('127.0.0.1') !== -1;
  }

  const getData = async () => {
    if (isLocalHost(window.location.hostname)) {
      console.warn("Development mode")
      await fetch("");
      return staticData;
    }

    const url: string = 'https://api.github.com/repos/italia-opensource/awesome-italia-innovative-companies/contents/website/src/data/outputs.json'
    const response = await fetch(url);
    const data_1 = await response.json();
    const encoding = data_1.encoding;
    let content = data_1.content;
    if (content) {
      if (encoding == "base64") {
        content = atob(content);
      }
      return JSON.parse(content);
    }
    console.warn("The data loaded in the table are taken from the static file generated at build time.");
    return staticData;
  }

  useEffect(() => {

    getData().then(result => {
      const markerList = [];
      result.data.map(company => (
        markerList.push(<Marker
          key={company.name}
          position={[
            company?.geometry?.coordinates[0] || 0.0,
            company?.geometry?.coordinates[1] || 0.0
          ]}
        >
          <Popup>
            <a href={company.site_url}>{company.name}</a>
            <br />
            {company.market}
          </Popup>
        </Marker>)
      )

      )
      setMarkerList(markerList)
    })


  }, [])

  return (

    <MapContainer center={romeLocation} zoom={5} scrollWheelZoom={false} style={{
      height: "500px", marginTop: "10px", marginBottom: '10px'
    }}>
      {markerList}
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
    </MapContainer>
  );

}