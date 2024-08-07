import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Tabs, Tab, Box } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import ReviewsIcon from '@mui/icons-material/RateReview';
import ImageSearchIcon from '@mui/icons-material/ImageSearch';

import About from './components/About';
import GetReviews from './components/GetReviews';
import ImageSearch from './components/ImageSearch';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            Tranquil Trails
          </Typography>
        </Toolbar>
        <Tabs value={false} variant="fullWidth">
          <Tab icon={<HomeIcon />} label="About" component={Link} to="/" />
          <Tab icon={<ReviewsIcon />} label="Get Reviews" component={Link} to="/get-reviews" />
          <Tab icon={<ImageSearchIcon />} label="Image Search" component={Link} to="/image-search" />
        </Tabs>
      </AppBar>
      <Box p={3}>
        <Routes>
          <Route path="/" element={<About />} />
          <Route path="/get-reviews" element={<GetReviews />} />
          <Route path="/image-search" element={<ImageSearch />} />
        </Routes>
      </Box>
    </Router>
  );
}

export default App;