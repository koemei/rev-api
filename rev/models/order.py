from rev.models.api_serializable import ApiSerializable


class OrderListPage(ApiSerializable):
    """
    Represents a paginated list of orders, including pagination info.
    attr_reader :total_count, :results_per_page, :page, :orders
    """

    def __init__(self, fields):
        """
        @param fields [Hash] hash of OrdersListPage fields parsed from JSON API response
        """
        super(OrderListPage, self).__init__(fields)


class Link(ApiSerializable):
    """
    Link to actual file represented by attachment
    """

    def __init__(self, fields):
        """
        @param fields [Hash] fields of attachment fields parsed from JSON API response
        """
        super(Link, self).__init__(fields)


class TranslationInfo(ApiSerializable):
    """
    Additional information specific to translation orders,
    such as word count, languages
    """

    def __init__(self, fields):
        """
        @param fields [Hash] fields of attachment fields parsed from JSON API response
        """
        super(TranslationInfo, self).__init__(fields)


class TranscriptionInfo(ApiSerializable):
    """
    Additional information specific to transcription orders,
    such as total length in minutes, verbatim and timestamps flags
    """

    def __init__(self, fields):
        """
        @param fields [Hash] fields of attachment fields parsed from JSON API response
        """
        super(TranscriptionInfo, self).__init__(fields)


class Comment(ApiSerializable):
    """
    Order comment, containing author, creation timestamp and text
    """

    def __init__(self, fields):
        """
        @param fields [Hash] hash of comment fields parsed from JSON API response
        """
        super(Comment, self).__init__(fields)
        self.timestamp = fields['timestamp']
        self.text = fields['text'] if 'text' in fields else '' # right now API gives no 'text' field if text is empty


class Attachment(ApiSerializable):
    """
    Represents order attachment - logical document associated with order
    attr_reader :kind, :name, :id, :audio_length, :word_count, :links
    """

    # List of supported mime-types used to request attachment's content
    # within 'Accept' header
    REPRESENTATIONS = {
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'doc': 'application/msword',
      'pdf': 'application/pdf',
      'txt': 'text/plain',
      'youtube': 'text/plain; format=youtube-transcript'
    }

    KINDS = {
        'transcript': 'transcript',
        'translation': 'translation',
        'media': 'media'
    }

    def __init__(self, fields):
        """
        @param fields [Hash] fields of attachment fields parsed from JSON API response
        """
        super(Attachment, self).__init__(fields)

        self.links = []
        for link in fields['links']:
            self.links.append(Link(fields=link))

    def representation_mime(self, ext):
        """
        @param ext [Symbol] extension
        @return [String] mime-type for requested extension
        """
        return self.REPRESENTATIONS[ext]


class Order(ApiSerializable):
    """
    Represents Translation or Transcription order.
    Should have TranslationInfo or TranscriptionInfo, list
    of comments and attachments. Attributes names reflect
    API exposed names, but occasional hyphens are replaced
    with underscores

    attr_reader :order_number, :price, :status, :attachments, :comments,
      :translation, :transcription, :client_ref

    @param fields [Hash] hash of order fields parsed from JSON API response
    """

    def __init__(self, fields):
        super(Order, self).__init__(fields)

        self.attachments = []
        for attachment in fields['attachments']:
            self.attachments.append(Attachment(fields=attachment))

        self.comments = []
        for comment in fields['comments']:
            self.comments.append(Comment(fields=comment))

        if 'translation' in fields:
            self.translation = TranslationInfo(fields=fields['translation'])
        if 'transcription' in fields:
            self.transcription = TranscriptionInfo(fields=fields['transcription'])

    @property
    def transcripts(self):
        """
        @return [Array of Attachment] with the kind of "transcript"
        """
        return [transcript for transcript in self.attachments if transcript.kind == Attachment.KINDS['transcript']]

    @property
    def translations(self):
        """
        @return [Array of Attachment] with the kind of "transcript"
        """
        return [translation for translation in self.attachments if translation.kind == Attachment.KINDS['translation']]

    @property
    def sources(self):
        """
        @return [Array of Attachment] with the kind of "transcript"
        """
        return [source for source in self.attachments if source.kind == Attachment.KINDS['media']]