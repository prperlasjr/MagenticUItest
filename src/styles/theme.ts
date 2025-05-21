export type Theme = {
  colors: {
    primary: string;
    secondary: string;
    success: string;
    danger: string;
    warning: string;
    info: string;
    background: string;
    surface: string;
    text: {
      primary: string;
      secondary: string;
      muted: string;
    };
    agent: {
      primaryBackground: string;
      primaryBorder: string;
      secondaryBackground: string;
      secondaryBorder: string;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  typography: {
    fontFamily: string;
    fontSize: {
      xs: string;
      sm: string;
      md: string;
      lg: string;
      xl: string;
    };
    fontWeight: {
      normal: number;
      medium: number;
      bold: number;
    };
  };
  borderRadius: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    circle: string;
  };
  shadows: {
    none: string;
    sm: string;
    md: string;
    lg: string;
  };
  transitions: {
    fast: string;
    normal: string;
    slow: string;
  };
};

export const lightTheme: Theme = {
  colors: {
    primary: '#2196f3',
    secondary: '#6c757d',
    success: '#4caf50',
    danger: '#f44336',
    warning: '#ff9800',
    info: '#03a9f4',
    background: '#f8f9fa',
    surface: '#ffffff',
    text: {
      primary: '#212529',
      secondary: '#6c757d',
      muted: '#999999',
    },
    agent: {
      primaryBackground: '#f1f8e9',
      primaryBorder: '#dcedc8',
      secondaryBackground: '#e3f2fd',
      secondaryBorder: '#bbdefb',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  typography: {
    fontFamily: "'-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      md: '1rem',
      lg: '1.25rem',
      xl: '1.5rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      bold: 700,
    },
  },
  borderRadius: {
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '16px',
    circle: '50%',
  },
  shadows: {
    none: 'none',
    sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
  },
  transitions: {
    fast: '0.15s ease',
    normal: '0.3s ease',
    slow: '0.5s ease',
  },
};

export const darkTheme: Theme = {
  colors: {
    primary: '#2196f3',
    secondary: '#6c757d',
    success: '#4caf50',
    danger: '#f44336',
    warning: '#ff9800',
    info: '#03a9f4',
    background: '#121212',
    surface: '#1e1e1e',
    text: {
      primary: '#e0e0e0',
      secondary: '#aaaaaa',
      muted: '#777777',
    },
    agent: {
      primaryBackground: '#1e3b29',
      primaryBorder: '#2e5d34',
      secondaryBackground: '#0e2e4a',
      secondaryBorder: '#164c7e',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  typography: {
    fontFamily: "'-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      md: '1rem',
      lg: '1.25rem',
      xl: '1.5rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      bold: 700,
    },
  },
  borderRadius: {
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '16px',
    circle: '50%',
  },
  shadows: {
    none: 'none',
    sm: '0 1px 3px rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px rgba(0, 0, 0, 0.3)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.3)',
  },
  transitions: {
    fast: '0.15s ease',
    normal: '0.3s ease',
    slow: '0.5s ease',
  },
};