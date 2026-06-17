from rest_framework import serializers


from rest_framework import serializers


class TransferSerializer(serializers.Serializer):

    source_account = serializers.CharField()
    destination_account = serializers.CharField()

    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    type = serializers.CharField()

    def validate(self, attrs):

        if attrs["amount"] <= 0:
            raise serializers.ValidationError(
                {
                    "amount": "Amount must be greater than zero."
                }
            )

        if (
            attrs["source_account"]
            == attrs["destination_account"]
        ):
            raise serializers.ValidationError(
                {
                    "destination_account":
                    "Source and destination accounts cannot be the same."
                }
            )

        return attrs
