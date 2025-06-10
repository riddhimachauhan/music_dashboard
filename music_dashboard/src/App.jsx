const baseUrl = import.meta.env.VITE_BACKEND_URL;
fetch(`${baseUrl}/api/tracks`)

import React, { useEffect, useState } from "react";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";
import CheckBoxOutlineBlankIcon from "@mui/icons-material/CheckBoxOutlineBlank";
import CheckBoxIcon from "@mui/icons-material/CheckBox";
import "./App.css";

const columns = [
  { key: "track", label: "Track" },
  { key: "artist", label: "Artist" },
  { key: "release_date", label: "Release Date" },
  { key: "streams", label: "Value" },
];

const sortOptions = [
  { key: "latest.spotify_plays", label: "Spotify Streams" },
  { key: "latest.spotify_playlist_count", label: "Spotify Playlist Count" },
  { key: "latest.spotify_popularity", label: "Spotify Popularity" },
  { key: "latest.spotify_playlist_total_reach", label: "Spotify Playlist Reach" },
];

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;

function App() {
 
  const [tracks, setTracks] = useState([]);
  const [filteredTracks, setFilteredTracks] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [genreOptions, setGenreOptions] = useState([]);
  const [selectedMoods, setSelectedMoods] = useState([]);
  const [moodOptions, setMoodOptions] = useState([]);
  const [selectedActivities, setSelectedActivities] = useState([]);
  const [activityOptions, setActivityOptions] = useState([]);
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [artistOptions, setArtistOptions] = useState([]);
  const [releaseDate, setReleaseDate] = useState("");
  const [releaseDateOption, setReleaseDateOption] = useState("All Time");
  const [sortKey, setSortKey] = useState("latest.spotify_plays");
  const [sortOrder, setSortOrder] = useState("desc");
  const [loading, setLoading] = useState(false);
  const [filterModalOpen, setFilterModalOpen] = useState(false);

  
  const handleArtistInputChange = (event, value) => {
    if (value) {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/artists?search=${encodeURIComponent(value)}`)
        .then(res => res.json())
        .then(data => setArtistOptions(data))
        .catch(err => console.error(err));
    }
  };

  const handleGenreInputChange = (event, value) => {
    if (value) {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/genres?search=${encodeURIComponent(value)}`)
        .then(res => res.json())
        .then(data => setGenreOptions(data))
        .catch(err => console.error(err));
    }
  };

  const handleMoodInputChange = (event, value) => {
    if (value) {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/moods?search=${encodeURIComponent(value)}`)
        .then(res => res.json())
        .then(data => setMoodOptions(data))
        .catch(err => console.error(err));
    }
  };

  const handleActivityInputChange = (event, value) => {
    if (value) {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api/activities?search=${encodeURIComponent(value)}`)
        .then(res => res.json())
        .then(data => setActivityOptions(data))
        .catch(err => console.error(err));
    }
  };

  
  useEffect(() => {
    if (releaseDateOption !== "All Time") return;
    const fetchTracks = async () => {
      setLoading(true);
      try {
        let params = [
          `sortColumn=${sortKey}`,
          `sortOrderDesc=${sortOrder === "desc"}`
        ];
        if (selectedGenres.length > 0) {
          params.push("genre_ids=" + selectedGenres.map((g) => g.id).join(","));
        }
        if (selectedMoods.length > 0) {
          params.push("mood_ids=" + selectedMoods.map((m) => m.id).join(","));
        }
        if (selectedActivities.length > 0) {
          params.push("activity_ids=" + selectedActivities.map((a) => a.id).join(","));
        }
        if (selectedArtist) {
          params.push("artist_id=" + selectedArtist.id);
        }
        let url = "";
        if (
          selectedGenres.length > 0 ||
          selectedMoods.length > 0 ||
          selectedActivities.length > 0 ||
          selectedArtist
        ) {
          url = import.meta.env.VITE_BACKEND_URL + "/api/tracks-by-filters?" + params.join("&");
        } else {
          url = `${import.meta.env.VITE_BACKEND_URL}/api/top-tracks?order=${sortOrder}`;
        }
        const res = await fetch(url);
        const data = await res.json();
        setTracks(data);
        setFilteredTracks(data);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    fetchTracks();
  }, [
    sortOrder,
    sortKey,
    selectedGenres,
    selectedMoods,
    selectedActivities,
    selectedArtist,
    releaseDateOption,
  ]);

  
  useEffect(() => {
    if (releaseDateOption === "All Time") return;
    setLoading(true);
    fetch(
      `${import.meta.env.VITE_BACKEND_URL}/api/tracks-by-release-date?filter_option=${encodeURIComponent(
        releaseDateOption
      )}&sortColumn=${sortKey}&sortOrderDesc=${sortOrder === "desc"}`
    )
      .then((res) => res.json())
      .then((data) => {
        setTracks(data);
        setFilteredTracks(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [releaseDateOption, sortKey, sortOrder]);

  
  useEffect(() => {
    let filtered = tracks;
    if (releaseDate) {
      filtered = filtered.filter((t) => t.release_date === releaseDate);
    }
    setFilteredTracks(filtered);
  }, [releaseDate, tracks]);

  const releaseDates = [...new Set(tracks.map((t) => t.release_date))];

  
  const modalStyle = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    background: "white",
    padding: 32,
    borderRadius: 16,
    boxShadow: "0 4px 32px rgba(0,0,0,0.15)",
    minWidth: 350,
    display: "flex",
    flexDirection: "column",
    gap: 24,
  };

  return (
    <div className="container">
      <h1>Top 50 Tracks</h1>

      <div className="controls" style={{ gap: 24 }}>
        {}
        <Button
          variant="contained"
          color="primary"
          onClick={() => setFilterModalOpen(true)}
        >
          Filter
        </Button>

        {/* Artist Autocomplete */}
        <Autocomplete
          options={artistOptions}
          getOptionLabel={(option) => option.label || option.name}
          value={selectedArtist}
          onChange={(event, newValue) => setSelectedArtist(newValue)}
          onInputChange={handleArtistInputChange}
          style={{ width: 250 }}
          renderInput={(params) => (
            <TextField {...params} label="Artist" placeholder="Type artist name..." />
          )}
        />

        {/* Release Date Filter */}
        <select
          value={releaseDateOption}
          onChange={(e) => setReleaseDateOption(e.target.value)}
          style={{ padding: 8, borderRadius: 8, border: "1px solid #c9c9c9" }}
        >
          <option value="Last 1 Week">Last 1 Week</option>
          <option value="Last 1 Month">Last 1 Month</option>
          <option value="Last 1 Year">Last 1 Year</option>
          <option value="All Time">All Time</option>
        </select>

        {/* Sort Options */}
        <select
          value={sortKey}
          onChange={(e) => setSortKey(e.target.value)}
          style={{ padding: 8, borderRadius: 8, border: "1px solid #c9c9c9" }}
        >
          {sortOptions.map((opt) => (
            <option key={opt.key} value={opt.key}>
              {opt.label}
            </option>
          ))}
        </select>

        <button
          onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
          
        >
          {sortOrder === "asc" ? "Ascending" : "Descending"}
        </button>
      </div>

      {}
      <Modal open={filterModalOpen} onClose={() => setFilterModalOpen(false)}>
        <div style={modalStyle}>
          <h2>Filter Tracks</h2>
          <Autocomplete
  multiple
  options={moodOptions}
  value={selectedMoods}
  isOptionEqualToValue={(option, value) => option.id === value.id}  // Important for object equality
  getOptionLabel={(option) => option.label || option.name || ""}  // Display the label or name property
  onChange={(event, newValue) => setSelectedMoods(newValue)}
  onInputChange={handleMoodInputChange}
  renderOption={(props, option, { selected }) => (
    <li {...props}>
      <Checkbox
        icon={icon}
        checkedIcon={checkedIcon}
        style={{ marginRight: 8 }}
        checked={selected}
      />
      {option.label || option.name}
    </li>
  )}
  style={{ width: 300 }}
  renderInput={(params) => (
    <TextField {...params} label="Moods" placeholder="Type to search..." />
  )}
/>

          
          <Autocomplete
  multiple
  options={activityOptions}
  value={selectedActivities}
  isOptionEqualToValue={(option, value) => option.id === value.id}
  getOptionLabel={(option) => option.label || option.name || ""}
  onChange={(event, newValue) => setSelectedActivities(newValue)}
  onInputChange={handleActivityInputChange}
  renderOption={(props, option, { selected }) => (
    <li {...props}>
      <Checkbox
        icon={icon}
        checkedIcon={checkedIcon}
        style={{ marginRight: 8 }}
        checked={selected}
      />
      {option.label || option.name}
    </li>
  )}
  style={{ width: 300 }}
  renderInput={(params) => (
    <TextField {...params} label="Activities" placeholder="Type to search..." />
  )}
/>

          {}
          <Autocomplete
            multiple
            options={genreOptions}
            value={selectedGenres}
            isOptionEqualToValue={(option, value) => option.id === value.id}
            onChange={(event, newValue) => setSelectedGenres(newValue)}
            onInputChange={handleGenreInputChange}
            renderOption={(props, option, { selected }) => (
              <li {...props}>
                <Checkbox
                  icon={icon}
                  checkedIcon={checkedIcon}
                  style={{ marginRight: 8 }}
                  checked={selected}
                />
                {option.label || option.name}
              </li>
            )}
            style={{ width: 300 }}
            renderInput={(params) => (
              <TextField {...params} label="Genres" placeholder="Type to search..." />
            )}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={() => setFilterModalOpen(false)}
          >
            Apply
          </Button>
        </div>
      </Modal>

      {}
      {loading ? (
        <div style={{ marginTop: 32 }}>Loading tracks...</div>
      ) : (
        <table>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredTracks.slice(0, 50).map((track, idx) => (
              <tr key={idx}>
                <td className="left-align">{track.track}</td>
                <td>{track.artist}</td>
                <td>{track.release_date}</td>
                <td>
                  {track[sortKey.split('.').pop()] ?? track.streams ?? track.score}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
