
from abc import abstractmethod, ABC

class BaseSnowflakeConnector(ABC):
    """
    Base class to manage Snowflake connections securely.
    """
    
    def __init__(self, user: str, password: str, account: str):
        """
        Initializes the base Snowflake connection.
        
        :param user: Snowflake username
        :param password: Snowflake password
        :param account: Snowflake account identifier
        """
        self.user = user
        self.password = password
        self.account = account
        self.connection = None

    @abstractmethod
    def connect(self):
        """Establishes a connection to Snowflake."""
        raise NotImplementedError()

    @abstractmethod
    def close_connection(self):
        """Closes the Snowflake connection."""
        raise NotImplementedError()