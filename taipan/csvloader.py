"""Package for loading CSV files."""

from csv import QUOTE_NONE, QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONNUMERIC, \
    Dialect, register_dialect, reader
import io
import _io
import uuid
import numpy


class CSVLoader(object):
    available_quote = [
        QUOTE_NONE, QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONNUMERIC
    ]
    quoting = QUOTE_MINIMAL
    delimiter = ","
    doublequote = False
    skipinitialspace = True
    lineterminator = '\n'

    def __init__(
        self,
        delimiter=",",
        quotechar='"',
        quoting=QUOTE_MINIMAL,
        doublequote=False,
        skipinitialspace=True,
        lineterminator='\n'
    ):
        self.set_delimiter(delimiter)
        self.set_quotechar(quotechar)
        self.set_quoting(quoting)
        self.set_doublequote(doublequote)
        self.set_skipinitialspace(skipinitialspace)
        self.set_lineterminator(lineterminator)
        self.dialect_id = str(uuid.uuid4())
        self.setup_dialect()

    def setup_dialect(self):
        class CSVDialect(Dialect):
            delimiter = self.delimiter
            quotechar = self.quotechar
            doublequote = self.doublequote
            skipinitialspace = self.skipinitialspace
            lineterminator = self.lineterminator
            quoting = self.quoting
        register_dialect(self.dialect_id, CSVDialect)

    def set_delimiter(self, delimiter):
        self.delimiter = delimiter

    def set_quotechar(self, quotechar):
        self.quotechar = quotechar

    def set_doublequote(self, doublequote):
        self.doublequote = doublequote

    def set_skipinitialspace(self, skipinitialspace):
        self.skipinitialspace = skipinitialspace

    def set_lineterminator(self, lineterminator):
        self.lineterminator = lineterminator

    def set_quoting(self, quoting):
        if not quoting in self.available_quote:
            raise Exception("It is not possible to set quoting to {}!".format(quoting))
        self.quoting = quoting

    def load_csv(self, str_or_file):
        """Load file descriptor or string io CSV to numpy array."""
        if isinstance(str_or_file, str):
            str_or_file = io.StringIO(str_or_file)
        elif isinstance(str_or_file, _io.TextIOWrapper):
            pass
        else:
            raise Exception("Pass a string or file descriptor to this method!")
        csv_reader = reader(str_or_file, dialect=self.dialect_id)
        csv = []
        for line in csv_reader:
            csv.append(line)
        return numpy.array(csv)
