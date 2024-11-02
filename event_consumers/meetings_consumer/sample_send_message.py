import time
import pika
import sys
import os
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

def send_message(channel):
    # Construct a sample JSON message
    message_data = {
        "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
        "title": "YvBEJnzgNpSHqRQrytdZuomeOSsOyAfpjwtnWbYspJCNmwsdmdXCcfMkkSlwTbDyboDkaKAywaJVbCHdOHeDVaVKpTDEcmTldLrvuLCQPqSpErvDFpQMvrQAIvQzprgJrjtrNqxTyrRgbSHyrTuaRJsroEIlFlGboIrMmUUAxEzMQhrLxFgWIVIsucKcEaoWAZmqbatfxZdixXgHMRVjaSzeqEVHGcTxvHSuYaKNQHfGwrEhEDxCzHTojsgwXSqadUgVkdzoJSyhSYoRMyPVwRhXzECwTKtZGFpOIRRzXNshYabdmrYfMRpRljRfmQVIXpZeUJWQzjqGmPLoYTvhlqyNNgTQEOWbrDfaPMRckUnLwUOyWWAAFiXBqlqLKxHHLtBxQrjIzZZMKfQYjhjSdsmroDxDTsRhOoKXCTvpqcLMghwmxeyLDmxayAfxAsZYyGfPpxmYOtXYbmIGTgpLvwKQlZuWpyllZyktaNcdotaUIEnelbsAqkDnjkdignBuKJDGJujqNEAKLLbbNfgiLjDDkTavItualShObwcMjrdSOdmKMlHgCQbJTydUJJhkubcRqCmbACzTzJihtHWnHbiWWtdLEPjqqTPTHYqCwByfILIlAbefRJiohpGXpNocMJzUWILXQWXPzSfgPBbkoVQTjndwORdMwjGarDURbFltlFoOcOTYWYvHALygapInJXRkzzYWSnzCCqmXBbasWwpkinFiaNxwjWuiwkJSsBbqnuJGjnLYrsZOKlpHNJNtlFKCpKRWKGsDhMJTGNRNtOdwPWNWweljyOjnqtvfaqFeXqvGZqlLrXAICsVOQAOiNivUoGcnkMFuhceaxivuUzFBBkztSktpsAWeRpKVSyJWJPoRuegeoiYIwIPRqAwvggNFjWwrnGUQRbFgapxSTyaEhoFpprFWShlrSlcCYiSHFSuGBIkxZWmpFwrzFjYOmGuOyUqENQFmrRLotfsjmNCXQfkpcSrWRFTpUIeojErRgkplUcTsbxCsVuNhhRVVysqceoYNJlUrkjcdejlwuQgJXXztADNHCZCspJPmmJhVzblOyrNwjJvKMjpNMKWlewmJhSgGwVdOtqzOJbLXSOPtIbwwPpaVRqWJmwIteXDmwNfDnZbgGhdvMVOLRxZpvYaEYGVYLcrYnLAUCvjOeYLfhdnKslsLFAtMUPgwRuGqIGFENipnLALIgHbReZjcCXQBtLVjFLhnvNyXBjfGhentoGJyvfwOOsRKNNeTBPoeyWlKtrWrfoforXvMbeMwxtHwfZSWAOdTljWsRLHUBBCIlgcPXlXYhjTNyRojmevMpNcMLqIboOpKjnapYVNyRaMAKQNjpdUrValIScyyIdplhhNAJiTXXINqbsGcoTiHuoKoRBYhwzAEGUlGkIVLCCkxnoGEmZlxFFJsRWrFDmfjrnnVmnsedekFIrJRXgBIGNlgKxXUVRpFihbRiscEBvBhFsHxsXBfYaezSPJdtfsEzFurbyOMqfocBuJGKuKlHeowKgMzzIptyMkHTLxQYcafACuofoKvjWNCPEzeBLWaEYBxuEWABTUnWnmCPCzrhNBNjYVdzbEtrRuTUQiVZomimVKvcllGGdiSXTUNbxvLUPjNasIBkiKtpzCISRFCqmeLyCyioSIdDdHjLsunhLvMFuZoBvIuwkTwaRcMyplHpEXFLjIcilZyvrSleyaQFSUEjbCkUHTgNpSqZOLckIozGlTvwuLPlZoWdEMjCzCaZqiVIPHmflqYiFGSVzWzYhnzRnIdqDCQuBUBFpFkXfZpFaQlYhHnbZLNGulAepXxNkbFXdZdQHbVRNYLLGvjvQkVhklyFTzFNZIKRitoANKaDfZemqUwsUAPXfsQfoEWDhGvuCZeItgcCjFPVcOhMOvcZOO",
        "date_time": "2024-11-15 07:50 PM",
        "location": "PzDjOsxnWqLWqomujrIuHNqTzjlgfQxSCAHnDpRSNXNfgSRQzyfjsuDdSajmpfgqquyJdlTRsUhfbeRSrxDPCBCOuKLVKRrvjzhHnIaOqjNEVrNDyaxDHSVGcvrqmEntDfiojdxEsSxvzImWQBbWDuFvzSnsEHhAWRYIaxmKJzoTYOJjFPtPunFqCiDquKmgxMWXAIuLcbFPbXJUiToFljAJLUkkYATXvILwusAKCtsIpQQrngtgUFRgncseIRoTsOGxUMIrxpwSKWITdSdsQBrtPxZwNcExCxwCUQicEoagOirjGxswaEXPWQAZgJGqCcSjMqxmLgAqulBUVuuRsFilTcymRYloGTHQXjbXivRNqcFsvvNJveYuGWgJUtvxsZvyVDpPyGfrtDhZfCccOZJYlsYpNxoqdMekgifamynSUUmOuJZWIAbHzhiREbyeVAFNmzKULJNTLahuYPqglWhKsZIVVJdIMPakezXQWtmQqQDglJEjNlOcjbyWSAAwrEaNcOLRFWwSDslENusCcjLyVJhQfaKiCKtugMoIaypnLCvdcTbVPdDGulKOFJztxDjWtBYqLFpAwDUDmZUNdoSCJUDMZVmkrjkNTqYndShAhyapjBeXfFzhzcwQXbsIwXqVeXHmgWggeogFSMtSLkCFFZjMDZlxCzwJOnZrHSBRogVPUPjdMhOfYPoSEJCdIzWqGgiHBBWXwfSPnTBlHoiJXAtStkmAmYmmXDSnKmXDlSAolqDalToedzKzNdUFgvJIqJtWKPaJtjmxmokGSfgSxjUHVbaUwRXSawglNDjKyJjIsQhFznouuhQfNsaFsHLMTIqaShnCGJyASEUBcBGyVuGFeuJeohjDrJfVMkyZlWZZiUBVWcxikoYbnmXryyphAqETYYdAwoKPjaWzNAqbVHFRfqnuqiKnTscOgxQlGDvyDvoNNNnXVleMzVVtGrFJZGqvJOZGwPcvcvMIehKOwddagElQfmNfpMBriFlXYQysoWcKksBejZSxdylXWhzjeDBYoKgnPoWxXTBlAYGpXOhNGiKcrRgwaLkYPZUwQJetyxTnkNsVloPpDXIXwbPWapQBFSfAsxybWsTGGZJTdExIUBNqLOchgsnJMuFraEjDTyjfAMaRhkfMtbheocdklmMnFOVhfivdwVtHPZxHUyyWPkOjlQHSKXcDQMEaIuRKZFzARihocXqQtTwmFCFDbwAEzBboYZGQqjXQMDypxznlOQHeWDnvijhSpXbkHkFxEdQFEOqsxMAZRIrwKpoWYeclTBOyeVBuRkToGYBgnWvsFJyEOctGvDqLbwPkimClClvytEggNrHLNnWBLbVYMnqzmNiSbhCgJUyxXZeEZtqzJeFeHfuvxeFDOFFsARbdGsrcTjxENgafhsOxsBUXdGHIqwfvOiNOBMigNCpxAlcpvWSSgSVkEkMQYNMZsLKUpOvUCbZxVBNa",
        "details": "WoswndVlADfTatuHrvtvNLMZxlAhxMJxTgekHQbIqCSLRFmfDNEmtrHPWYSPtFuRnNZvKJixMYtjmYBCRPFpOLNJSHdniyiSpIxYQcnQKPGhONujAsCJQGIpYSVRIsicIHBIpcNsxBbWjbmowRMkoVIjguLnnJwXqhPEGQWgjMurTPRaBKZJVBAMLfuJfQklReTdCKAuuxdeMlrFquoHUGCVipWAOyWlgztOhhJVvKxDTpmWSondATdSfjIHonvdoGxIXYtehFRyalGyIwmNJrJEKpAHMeRcQQSXzGyRmURaRDljvgxgaBpRWBTZXcvJNyuNjKBiDyzAvsMOHNcAepfiUSYwLPnNcSdlFUYyzhMVNIKfZMyRHEjinpmsfUdlrrWthJlpDHGDZEyixsrvmKPrkdusflRTFnDyFKJapKtJXmxFZhHuJBfaVKFsdjJOiFXPGgbphRKagwhHEIcKlsGvFahurktvBMikIzyXxxAtXfpfXmDSWxZATYlUDAXDatjTJNMmEmxXeMsKahtoPSepQpUwxqRPqfFPBgkVsCsKJZfVYGoDluAKLbnarwgujZuFLHFSTlPYMdtZwEhWeOqKOVFTwxHQZLomEvKHQbpwDcazBigQPUqekgpvpnrPpMqufkaOXYBIyjHhtrUkucqJXknklpLzQFlfHZIKgTHSipkbvYwXdroTmOtVKyjiHscrXkgwYNXxyUoKWjdcaSIRvtwjPtbkSWRkfjWtgDwVTTUbNDdKLYQPKyVGTJPINvzwtKXVHkdGbfwnDvtXykIaHvcUisRyMfWQsNLCHriGUtgkkVFjGkAaRAEVfkFHiXLkWrnLfKnChLvEoRNDNYNfXnmRhkFAzUcDRvhZrVlfqYsNAJbGswhsUQEkdYplngCZQQAXuFADadAsDMulOXBthreufTFoUvSHdCduKleNzNARXHUUPrWROLNOJsUMeBBeZwreikAWpHuQXGnkfqEGzFXUrZNRtAipnvopYVnCgKlUDWmsAillGggKFSVdGJYCveZjOcovvxChkDqwDsIZijBCTfEOTOCeqflDrPiruMBTHGByzvxAqYFYYnCRzStXzbQRbjUkTtRQqEyjyRuhqkBjHyyrpRoRACUmmPovaXTvuEQEBPlWtGPoyiGEYQCYtewCcexxwfjXAbFtfQGJDhxRpACscrNNkeHntjKBsNobBpMvDszDnZUdzALRcHNERujZbHTawihNOSiDLPaehPREjjzJlseeSbTBAMLJjdVvnEozropHloyAeSByTXIRbPNmMdTTUcFRCjHInumMBWqCHsPgFbOxuZMvxozChyPLfBpejFoDgdTmyyzPeatFdOLORCKuYEHExHVivaAHVUJMSHzkcDLSJzwVmTpFprmxOOzJZCemgzhgRBYfdHszdcetTXHCNjuqhTQEoIJIHoTxqMKmiJNHapyqqWvfjsfeSeQqVoIuIBwoTbmiQOXnaSbXRcmZurdWrsXXxgcCMmTpwAqFLABNuQHDYieGGFbVlNEtXcrnIXNzqqkfADbUXATtorcMdwBKXIdxQzgWQUIoVMvSmFeKIcSdjfDHmhsPmqfgHfgfWfUnNcyLQBJiCjsNNQqaqrDogFHYszdCKmReLKmtIkaPwHOeBTVJdbkUearhivuzPWzSvFzSIEwGHRLUaFxpqnLirRyPvDlezHQZpwzJYCyCfBljHnyaUhGMkCPtUHaxNKLjMerEyLARlaeSLNudVrUmjIcLTwGMUUQKAyMGUeCjdHvqYMPJjmoijRQBBVZjPRRTyaIAVwoawYRVqgIEDqSDmSQPBXHmgTGCHvExrXRbhpnZonDdWfNTkZAuTQykuqkgyDyxDEzXnWtmvFNGssKEXARVuwFfJnedYEjvnqMffsYHzbxwAROXbtNmPfImTybGjxUJTvaRyWWDhRIQfUaYeiYUgOKmXTabmdaVpOHWrYUvDPkwyYWrYhZcyIhawOUvNtNcAagZtazdpxsHrnxVTWZXPJCbdgaQSathzCeflVNZDFdoymJtkGexguAGWghEwgTaCKZYJffytRjDZifOroqyDltJiAfMnHMTLxTLLjEnxNAfrosVIdXTDtKEUWenkOXNeTSISowTTThnKoODDWZFrbPuGwRBTYQlxCsNhQHrPoBSwAOLwulERGYnaSLwarjDiLAUeMXzbCMtktRqnhinq",
        "participants": [
            {
                "participant_id": "162687d8-3073-48aa-8c85-b975f270c508",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "BabGFQIkYKLzwZnxuBWacjkzGCji",
                "email": "GZenG@example.com"
            },
            {
                "participant_id": "794214e4-8f08-4a73-8be3-e799c39af72d",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "uSbXmrXtmvcTvsYnGqMsghVbDfbJEnJvDEVbTLiQv",
                "email": "LcMjk@example.com"
            },
            {
                "participant_id": "2b1fbf6c-6223-44be-a493-a93392f66630",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "zJtVNitGVRgCyIkLnuWWDI",
                "email": "OUDmB@example.com"
            },
            {
                "participant_id": "7c63485b-15c5-40bb-955a-eba83748ae0d",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "fgQuLowVfscwssIdlAoDqpydUkomGjfIUGAYFgPT",
                "email": "xwkWP@example.com"
            },
            {
                "participant_id": "22e819e3-b917-4be4-ab56-a349fa770c1a",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "iWvdvZOMEQwhrgRrcEOIRWAxfTDyXtxbxEiaBykV",
                "email": "ZuzCk@example.com"
            },
            {
                "participant_id": "82282262-4894-489c-844d-2515b707f756",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "EpnHDHENLNUTcWuamaYvgc",
                "email": "xSShk@example.com"
            },
            {
                "participant_id": "77b61586-e842-4114-bb98-e9669c94392f",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "rCUnsJNBHlAdWtNQObZsFOULGuVuuqiqxGvEqolvFprRCUgNTYZVRthLdervCxDMOqZyKHqnqGFAmjYxVjwhCLpNlNgUdsNvGbKvYmTFNhGgRhSWiWMdNuXgGjkWDiNiJMBCvDmHCHwAXfzBmGmSROcEfiLkTtfmmPDCsqmKujjLEVgjOkTyNqgYuRwaCUykPTDmyRZIbxPdELehmExPQabJlTCITkYEaqbKanCQJwKjumEDevyDfmFqOtdcYywxxMnRydGgphtSPGZmhnMxRMwSlidYKLeVvVtCXDDDOswnAxGoSrfxEriyPaakOjEnXtmpUDhnvgUlVEZxUnUd",
                "email": "Submt@example.com"
            },
            {
                "participant_id": "0834b95c-87de-4652-8abe-6a857df3c4e4",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "tQecqSJYyxClexxdzAGgroTdUizyvvCWyoe",
                "email": "JcObh@example.com"
            },
            {
                "participant_id": "17786f0e-c18b-46e2-b4c7-7d8ebe927353",
                "meeting_id": "2dfb8bcc-dc4d-496b-be45-f50fb385e6fe",
                "name": "kaxiKOFHrXUtgTrNBipspagDUwgcxgSxPoWbaRBoaPUFDS",
                "email": "ZxJwU@example.com"
            },
        ]
    }

    # Convert the message to a JSON string
    message = json.dumps(message_data)

    # Publish the message to the "meetings" queue
    channel.basic_publish(
        exchange='',
        routing_key='meetings',
        body=message
    )
    logger.info(f"Sent message: {message}")

def main():
    connected = False
    connection = None
    channel = None

    # Retry logic to connect to RabbitMQ
    while not connected:
        try:
            credentials = pika.PlainCredentials("rabbituser", "rabbitpassword")
            parameters = pika.ConnectionParameters("message_broker", 5672, "demo-vhost", credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            logger.info("Connected to RabbitMQ")
            connected = True
        except pika.exceptions.AMQPConnectionError:
            logger.warning(f"Connection attempt failed, retrying in 5 seconds...")
            time.sleep(5)

    # Call the send_message function
    send_message(channel)

    # Clean up
    connection.close()
    logger.info("Connection closed.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted by user, exiting...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
