// Small hand-picked line-icon set — no external icon library required.
// Every icon takes `size` and forwards other svg props.

const base = (size) => ({
  width: size,
  height: size,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.6,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
});

export function HeartRatingIcon({ size = 16, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M12 20s-7-4.4-9.5-9C.8 7.4 2.6 4 6 4c2 0 3.4 1.1 4 2.2C10.6 5.1 12 4 14 4c3.4 0 5.2 3.4 3.5 7-2.5 4.6-9.5 9-9.5 9Z" />
    </svg>
  );
}

export function PinIcon({ size = 16, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M12 21s7-6.3 7-11.5A7 7 0 0 0 5 9.5C5 14.7 12 21 12 21Z" />
      <circle cx="12" cy="9.5" r="2.4" />
    </svg>
  );
}

export function UsersIcon({ size = 16, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <circle cx="9" cy="8" r="3" />
      <path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" />
      <path d="M16 4.2c1.7.5 3 2.1 3 3.8s-1.3 3.3-3 3.8" />
      <path d="M21 20c0-2.8-2-5.1-4.7-5.8" />
    </svg>
  );
}

export function BedIcon({ size = 16, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M2 18v-6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v6" />
      <path d="M2 18v2" />
      <path d="M22 18v2" />
      <path d="M2 13v-1a3 3 0 0 1 3-3h6" />
      <circle cx="7" cy="10" r="1.4" />
    </svg>
  );
}

export function AreaIcon({ size = 16, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <rect x="4" y="4" width="16" height="16" rx="1" />
      <path d="M4 9h2" />
      <path d="M4 15h2" />
      <path d="M9 4v2" />
      <path d="M15 4v2" />
    </svg>
  );
}

export function BathIcon({ size = 16, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M4 12h16v2a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5v-2Z" />
      <path d="M6 12V6a2 2 0 0 1 3.5-1.3" />
      <path d="M4 19l-1 2" />
      <path d="M20 19l1 2" />
    </svg>
  );
}

export function ChevronLeftIcon({ size = 20, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M15 18l-6-6 6-6" />
    </svg>
  );
}

export function ChevronRightIcon({ size = 20, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M9 18l6-6-6-6" />
    </svg>
  );
}

export function StarIcon({ size = 14, ...p }) {
  return (
    <svg {...base(size)} fill="currentColor" stroke="none" {...p}>
      <path d="M12 2.5l2.9 6 6.6.7-4.9 4.5 1.3 6.5L12 16.9l-5.9 3.3 1.3-6.5-4.9-4.5 6.6-.7L12 2.5Z" />
    </svg>
  );
}

export function ThumbUpIcon({ size = 15, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M7 10v10H4a1 1 0 0 1-1-1v-8a1 1 0 0 1 1-1h3Z" />
      <path d="M7 10l3.5-7a2 2 0 0 1 2 2v4h5.2a2 2 0 0 1 2 2.4l-1.4 6A2 2 0 0 1 16.4 19H10a3 3 0 0 1-3-3" />
    </svg>
  );
}

export function ThumbDownIcon({ size = 15, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <path d="M17 14V4h3a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-3Z" />
      <path d="M17 14l-3.5 7a2 2 0 0 1-2-2v-4H6.3a2 2 0 0 1-2-2.4l1.4-6A2 2 0 0 1 7.6 5H14a3 3 0 0 1 3 3" />
    </svg>
  );
}

// Generic amenity glyph fallback (used when an amenity has no uploaded icon image).
export function AmenityDotIcon({ size = 14, ...p }) {
  return (
    <svg {...base(size)} {...p}>
      <circle cx="12" cy="12" r="3" />
      <path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1" />
    </svg>
  );
}
EOF