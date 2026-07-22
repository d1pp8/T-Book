import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import { RequireAuth, RequireOwner } from './components/Guards';

import Home from './pages/Home';
import ListingDetail from './pages/ListingDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import GuestBookings from './pages/GuestBookings';
import OwnerProperties from './pages/OwnerProperties';
import OwnerPropertyDetail from './pages/OwnerPropertyDetail';
import OwnerUnitDetail from './pages/OwnerUnitDetail';
import OwnerBookings from './pages/OwnerBookings';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/listings/:propertyUuid" element={<ListingDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/profile" element={<RequireAuth><Profile /></RequireAuth>} />
        <Route path="/bookings" element={<RequireAuth><GuestBookings /></RequireAuth>} />

        <Route path="/owner/properties" element={<RequireOwner><OwnerProperties /></RequireOwner>} />
        <Route path="/owner/properties/:propertyUuid" element={<RequireOwner><OwnerPropertyDetail /></RequireOwner>} />
        <Route path="/owner/properties/:propertyUuid/units/:unitUuid" element={<RequireOwner><OwnerUnitDetail /></RequireOwner>} />
        <Route path="/owner/bookings" element={<RequireOwner><OwnerBookings /></RequireOwner>} />

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
