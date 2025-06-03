import React, { useEffect, useState } from "react";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import Checkbox from "@mui/material/Checkbox";
import CheckBoxOutlineBlankIcon from "@mui/icons-material/CheckBoxOutlineBlank";
import CheckBoxIcon from "@mui/icons-material/CheckBox";
import "./App.css";

const columns = [
  { key: "track", label: "Track" },
  { key: "artist", label: "Artist" },
  { key: "release_date", label: "Release Date" },
  { key: "streams", label: "Streams" },
];

const sortOptions = [
  { key: "streams", label: "Streams" },
  { key: "playlist_count", label: "Playlist Count" },
  { key: "popularity", label: "Popularity" },
  { key: "playlist_reach", label: "Playlist Reach" },
];

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;

function App() {
  const [tracks, setTracks] = useState([]);
  const [filteredTracks, setFilteredTracks] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [genreOptions, setGenreOptions] = useState([]);
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [artistOptions, setArtistOptions] = useState([]);
  const [releaseDate, setReleaseDate] = useState("");
  const [sortKey, setSortKey] = useState("streams");
  const [sortOrder, setSortOrder] = useState("desc");
  const [loading, setLoading] = useState(false);

  // Fetch artist options on input change
  const handleArtistInputChange = (event, value) => {
    if (value) {
      fetch(`http://localhost:5000/api/artists?search=${encodeURIComponent(value)}`)
        .then(res => res.json())
        .then(data => setArtistOptions(data))
        .catch(err => console.error(err));
    }
  };

  // Fetch genre options on input change
  const handleGenreInputChange = (event, value) => {
    if (value) {
      fetch(`http://localhost:5000/api/genres?search=${encodeURIComponent(value)}`)
        .then(res => res.json())
        .then(data => setGenreOptions(data))
        .catch(err => console.error(err));
    }
  };

  // Fetch tracks based on filters
  useEffect(() => {
    const fetchTracks = async () => {
      setLoading(true);
      try {
        let url = "";

        if (selectedArtist) {
          url = `http://localhost:5000/api/tracks-by-artist?artist_id=${selectedArtist.id}`;
        } else if (selectedGenres.length > 0) {
          const genreIds = selectedGenres.map((g) => g.id).join(",");
          url = `http://localhost:5000/api/tracks-by-genres?genre_ids=${genreIds}`;
        } else {
          url = `http://localhost:5000/api/top-tracks?order=${sortOrder}`;
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
  }, [sortOrder, selectedGenres, selectedArtist]);

  // Filter tracks by release date
  useEffect(() => {
    let filtered = tracks;
    if (releaseDate) {
      filtered = filtered.filter((t) => t.release_date === releaseDate);
    }
    setFilteredTracks(filtered);
  }, [releaseDate, tracks]);

  // Sort tracks by selected key
  useEffect(() => {
    const sorted = [...filteredTracks].sort((a, b) => {
      if (sortOrder === "asc") return a[sortKey] > b[sortKey] ? 1 : -1;
      return a[sortKey] < b[sortKey] ? 1 : -1;
    });
    setFilteredTracks(sorted);
  }, [sortKey, sortOrder]);

  const releaseDates = [...new Set(tracks.map((t) => t.release_date))];

  return (
    <div className="container">
      <h1>Top 50 Tracks</h1>

      <div className="controls" style={{ gap: 24 }}>
        {/* Genre Multi-Select */}
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
              {option.label}
            </li>
          )}
          style={{ width: 250 }}
          renderInput={(params) => (
            <TextField {...params} label="Genres" placeholder="Type to search..." />
          )}
        />

        {/* Artist Autocomplete */}
        <Autocomplete
          options={artistOptions}
          getOptionLabel={(option) => option.label}
          value={selectedArtist}
          onChange={(event, newValue) => setSelectedArtist(newValue)}
          onInputChange={handleArtistInputChange}
          style={{ width: 250 }}
          renderInput={(params) => (
            <TextField {...params} label="Artist" placeholder="Type artist name..." />
          )}
        />

        {/* Release Date Dropdown */}
        <select
          value={releaseDate}
          onChange={(e) => setReleaseDate(e.target.value)}
          style={{ padding: 8, borderRadius: 8, border: "1px solid #c9c9c9" }}
        >
          <option value="">Filter by Release Date</option>
          {releaseDates.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>

        {/* Sort Key Dropdown */}
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

        {/* Sort Order Button */}
        <button
          onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
          style={{
            padding: "8px 16px",
            borderRadius: 8,
            border: "none",
            background: "#4f8cff",
            color: "#fff",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          {sortOrder === "asc" ? "Ascending" : "Descending"}
        </button>
      </div>

      {/* Table */}
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
                <td>{track.streams}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
