declare var require: any
import BrowserOnly from '@docusaurus/BrowserOnly';
import 'leaflet/dist/leaflet.css';
import React from 'react';

import staticData from "../../data/outputs.json";

function isLocalHost(url: string) {
  return url.indexOf('localhost') !== -1 || url.indexOf('127.0.0.1') !== -1;
}

const getData = async () => {
  if (isLocalHost(window.location.hostname)) {
    console.warn("Development mode")
    return staticData
  }

  const url: string = 'https://api.github.com/repos/italia-opensource/awesome-italia-innovative-companies/contents/website/src/data/outputs.json'
  const response = await fetch(url);
  const data = await response.json();
  const encoding = data.encoding;
  let content = data.content;
  if (content) {
    if (encoding == "base64") {
      content = atob(content);
    }
    return JSON.parse(content);
  }
  console.warn("The data loaded in the table are taken from the static file generated at build time.");
  return staticData;
}



export default function Map(): JSX.Element {

  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => {
        const MapContainer = require('react-leaflet').MapContainer;
        const TileLayer = require('react-leaflet').TileLayer;
        const Marker = require('react-leaflet').Marker;
        const Popup = require('react-leaflet').Popup;
        const L = require('leaflet');

        const romeLocation = [41.9028, 12.4964];

        const markerList: typeof Marker[] = [];

        getData().then(result => {
          result.data.map((company, idx) => (
            markerList.push(<Marker
              key={idx}
              position={[
                company?.geometry?.coordinates[0] || 0.0,
                company?.geometry?.coordinates[1] || 0.0
              ]}
              icon={L.icon({
                iconSize: [25, 41],
                iconAnchor: [10, 41],
                popupAnchor: [2, -40],
                iconUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-icon.png",
                shadowUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-shadow.png"
              })}
            >
              <Popup>
                <a href={company.site_url}>{company.name}</a>
                <br />
                {company.market}
              </Popup>
            </Marker>)
          ))
        });

        return <MapContainer center={romeLocation} zoom={5} scrollWheelZoom={false} style={{
          height: "500px", marginTop: "10px", marginBottom: '10px'
        }}>
          {markerList}
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          />
        </MapContainer>;
      }}
    </BrowserOnly>
  );
}