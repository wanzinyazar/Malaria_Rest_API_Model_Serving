import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import UploadFile from './components/UploadFile'
import ImagePreview from './components/ImagePreview'
import DraggableUploader from './components/DraggableUploader'
import Dropzone from 'react-dropzone'
import Table from './components/Table'

class App extends Component {
  render() {
    return (
      <div className="App">        
        <DraggableUploader />
        {/* <UploadFile /> */}
        
      </div>
    );
  }
}

export default App;
